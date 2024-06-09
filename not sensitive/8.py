def check_ml(data, n_run, knn, n_fold, n_proportion, n_subset, model_type, prediction_type, features, recalculate_similarity, disjoint_cv, split_both=False, output_file = None, model_fun = None, verbose=False, n_seed = None):
    drugs, disease_to_index, drug_to_values, se_to_index, drug_to_values_se, drug_to_values_structure, drug_to_values_target, drug_interaction_to_index, drug_to_values_interaction = data
    if prediction_type == "disease":

        disease_to_drugs, pairs, classes = utilities.get_drug_disease_mapping(drugs, drug_to_values, disease_to_index)
    elif prediction_type == "side effect":

        disease_to_drugs, pairs, classes = utilities.get_drug_disease_mapping(drugs, drug_to_values_se, se_to_index)
        drug_to_values_se = drug_to_values
        se_to_index = disease_to_index
    elif prediction_type == "drug interaction":
        if drug_interaction_to_index is None:
            raise ValueError("Drug interaction information is missing!")

        disease_to_drugs, pairs, classes = utilities.get_drug_disease_mapping(drugs, drug_to_values_interaction, drug_interaction_to_index)
    else:
        raise ValueError("Uknown prediction_type: " + prediction_type)
    list_M_similarity = []
    if "phenotype" in features:
        drug_to_index, M_similarity_se = utilities.get_similarity(drugs, drug_to_values_se)
        list_M_similarity.append(M_similarity_se)
    if "chemical" in features:
        drug_to_index, M_similarity_chemical = utilities.get_similarity(drugs, drug_to_values_structure)
        list_M_similarity.append(M_similarity_chemical)
    if "target" in features:
        drug_to_index, M_similarity_target = utilities.get_similarity(drugs, drug_to_values_target)
        list_M_similarity.append(M_similarity_target)
    if output_file is not None:
        output_f = open(output_file, 'a')
        output_f.write("n_fold\tn_proportion\tn_subset\tmodel type\tprediction type\tfeatures\trecalculate\tdisjoint\tpairwise\tvariable\tauc.mean\tauc.sd\tauprc.mean\tauprc.sd\n")
    else:
        output_f = None
    values = []
    values2 = []
    for i in xrange(n_run): 
        if n_seed is not None:
            n_seed += i
            random.seed(n_seed)
            numpy.random.seed(n_seed)
        pairs_, classes_, cv = utilities.balance_data_and_get_cv(pairs, classes, n_fold, n_proportion, n_subset, disjoint = disjoint_cv, split_both=split_both, n_seed = n_seed)
        val, val2 = check_ml_helper(drugs, disease_to_drugs, drug_to_index, list_M_similarity, pairs_, classes_, cv, knn, n_fold, n_proportion, n_subset, model_type, prediction_type, features, recalculate_similarity, disjoint_cv, split_both, output_f, model_fun, verbose, n_seed)
        values.append(val)
        values2.append(val2)
    print "AUC over runs: %.1f (+/-%.1f):" % (numpy.mean(values), numpy.std(values)), map(lambda x: round(x, ndigits=1), values)
    if output_f is not None:
        output_f.write("%d\t%d\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%f\t%f\t%f\t%f\n" % (n_fold, n_proportion, n_subset, model_type, prediction_type, "|".join(features), recalculate_similarity, disjoint_cv, split_both, "avg", numpy.mean(values), numpy.std(values), numpy.mean(values2), numpy.std(values2)))
        output_f.close()
    return "AUC: %.1f" % numpy.mean(values), "AUPRC: %.1f" % numpy.mean(values2)
