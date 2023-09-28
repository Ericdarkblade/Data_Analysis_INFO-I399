import numpy as np


list_of_features = np.genfromtxt(
    "Anna Help\\list_of_features.csv", delimiter=',', dtype=str)


def get_features_map():
    features_map = {}
    for index, feature in enumerate(list_of_features[1:, 0]):
        if feature == '':
            continue
        else:
            # +1 so that the index matches the array index, (we skipped headers)
            features_map[feature] = index + 1

    return features_map


def get_genotypes(feature, features_map):
    feature_row = features_map[feature]
    genotype_column = 3
    max_genotypes_column = 4
    max_genotypes = int(list_of_features[feature_row, max_genotypes_column])

    genotypes = []
    for iterator in range(max_genotypes):
        genotypes.append(
            list_of_features[feature_row + iterator, genotype_column])

    return genotypes


def get_phenotype(feature, features_map, genotype, genotypes):
    feature_row = features_map[feature]
    phenotype_column = 5
    phenotype_row = feature_row + genotypes.index(genotype)
    return list_of_features[phenotype_row, phenotype_column]


def assignment():
    features_map = get_features_map()

    print("FEATURES")
    print("----------------")
    for feature in features_map:
        print(feature)
    print('\n\n')
    selected_feature = ''
    try:
        selected_feature = input("Please Select a Feature (case sensitive): ")
        genotypes = get_genotypes(selected_feature, features_map)
    except:
        print("An invalid Feature was entered")
        return

    print("GENOTYPES")
    print("----------------")
    for genotype in genotypes:
        print(genotype)
    print('\n\n')

    selected_genotype = ''
    try:
        selected_genotype = input(
            "Please select a genotype (case sensitive): ")
        print("Your Phenotype is:")
        print("------------------------")
        print(get_phenotype(selected_feature,
              features_map, selected_genotype, genotypes))
        print("------------------------")
    except:
        print("An invalid genotype was entered")
        return


while True:
    assignment()
    response = input("Would you like to continue (Yes/no)").strip().upper()
    if response[0] != 'Y':
        break
