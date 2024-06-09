  return lat, long

def get_origin_lat_long():
  rospy.loginfo("Waiting for a message to initialize the origin GPS location...")
  origin_pose = rospy.wait_for_message('local_xy_origin', PoseStamped)
  origin_lat = origin_pose.pose.position.y
  origin_long = origin_pose.pose.position.x
  rospy.loginfo('Received origin: lat %s, long %s.' % (origin_lat, origin_long))
  return origin_lat, origin_long

def calc_goal(origin_lat, origin_long, goal_lat, goal_long):
  geod = Geodesic.WGS84 
  g = geod.Inverse(origin_lat, origin_long, goal_lat, goal_long)
  hypotenuse = distance = g['s12'] 
  rospy.loginfo("The distance from the origin to the goal is {:.3f} m.".format(distance))
  azimuth = g['azi1']
  rospy.loginfo("The azimuth from the origin to the goal is {:.3f} degrees.".format(azimuth))


  azimuth = math.radians(azimuth)
  x = adjacent = math.cos(azimuth) * hypotenuse
  y = opposite = math.sin(azimuth) * hypotenuse
  rospy.loginfo("The translation from the origin to the goal is (x,y) {:.3f}, {:.3f} m.".format(x, y))

  return x, y

class GpsGoal():
  def __init__(self):
    rospy.init_node('gps_goal')

    rospy.loginfo("Connecting to move_base...")
    self.move_base = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    self.move_base.wait_for_server()
    rospy.loginfo("Connected.")

    rospy.Subscriber('gps_goal_pose', PoseStamped, self.gps_goal_pose_callback)
    rospy.Subscriber('gps_goal_fix', NavSatFix, self.gps_goal_fix_callback)

    self.origin_lat, self.origin_long = get_origin_lat_long()

  def do_gps_goal(self, goal_lat, goal_long, z=0, yaw=0, roll=0, pitch=0):
    x, y = calc_goal(self.origin_lat, self.origin_long, goal_lat, goal_long)

    self.publish_goal(x=x, y=y, z=z, yaw=yaw, roll=roll, pitch=pitch)

  def gps_goal_pose_callback(self, data):
    lat = data.pose.position.y
    long = data.pose.position.x
    z = data.pose.position.z
    euler = tf.transformations.euler_from_quaternion(data.pose.orientation)
    roll = euler[0]
    pitch = euler[1]
    yaw = euler[2]
    self.do_gps_goal(lat, long, z=z, yaw=yaw, roll=roll, pitch=pitch)

  def gps_goal_fix_callback(self, data):
    self.do_gps_goal(data.latitude, data.longitude)

  def publish_goal(self, x=0, y=0, z=0, yaw=0, roll=0, pitch=0):

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = rospy.get_param('~frame_id','map')
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.position.z =  z
    quaternion = tf.transformations.quaternion_from_euler(roll, pitch, yaw)
    goal.target_pose.pose.orientation.x = quaternion[0]
    goal.target_pose.pose.orientation.y = quaternion[1]
    goal.target_pose.pose.orientation.z = quaternion[2]
    goal.target_pose.pose.orientation.w = quaternion[3]
    rospy.loginfo('Executing move_base goal to position (x,y) %s, %s, with %s degrees yaw.' %
            (x, y, yaw))
    rospy.loginfo("To cancel the goal: 'rostopic pub -1 /move_base/cancel actionlib_msgs/GoalID -- {}'")


    self.move_base.send_goal(goal)
    rospy.loginfo('Inital goal status: %s' % GoalStatus.to_string(self.move_base.get_state()))
    status = self.move_base.get_goal_status_text()
    if status:
      rospy.loginfo(status)


    self.move_base.wait_for_result()
    rospy.loginfo('Final goal status: %s' % GoalStatus.to_string(self.move_base.get_state()))
    status = self.move_base.get_goal_status_text()
    if status:
      rospy.loginfo(status)

@click.command()
@click.option('--lat', prompt='Latitude', help='Latitude')
@click.option('--long', prompt='Longitude', help='Longitude')
@click.option('--roll', '-r', help='Set target roll for goal', default=0.0)
@click.option('--pitch', '-p', help='Set target pitch for goal', default=0.0)
@click.option('--yaw', '-y', help='Set target yaw for goal', default=0.0)
def cli_main(lat, long, roll, pitch, yaw):