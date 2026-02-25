import numpy as np

class DefaultParameters:
    

    shots = 1024

    mutantNumber = 0
    
    userOnlyQiskitCode = False

    useIBMBackEndService = False

    justCalculateJobTime = False
    #not working and need inspection
    usePrecomputedKernel = False

    #not used anymore
    useParametersClassParameters = True

    roundNumber = 1

    inputNumber = 1

    showProgressDetails = True

    n_folds = 5
    # n_folds = 15
    # 0 = wine data, 1 = load digits, 2 = credit card. 3 = mnist, 4= custom
    # dataType = 0
    
    dataType = 0

    #0 = amplitude embedding, 1 = angle embedding, 2 = custom embedding
    featureMapType = 0

    amplitudeNQubits = 4
    angleNQubits = 13
    phasenqubits = 5

    alwaysUsePCA = True 

    # pca_components = 8
    pca_components = 8

    applyMRs = True

    mrUsed = 1
    
    AskUserToApplyMRs = False

    askUserToInputParameters = False

    applyScalarValue = True
    scaleValue = 5.0

    fromScaleValue = 11

    # toScaleValue = 20
    toScaleValue = 12
    
    applyAngleRotation = False

    # angle = 2* np.pi 
    # angle = np.pi 
    angle = np.pi/4
    angle = 5

    applyPermutation = False

    invertAllLabels = False
    numberOfLabelsClasses = 3

    inputToDuplicate = 1

    #mr6
    addQuantumRegister = False

    #mr7
    injectNullEffectOperation = False

    #mr8
    injectParameter = False

    #mr9
    changeDevice = False

    #mr10
    changeOptimization = False

    #mr11
    reverseWires = False

    #mr12
    reverseQubitsMultiplication = False

    #mr13
    checkSymmetry = False
    
    #mr14
    checkSameInputSymmetry = False

    #mr15 
    checkScalingInvariance = False

    #mr16
    checkAddingPeriodicity = False

    #mr16
    checkShiftingInvariance = False

    applyPerturbNoise = False
    perturbNoise = 0.1

    circuitDepth = 2
    applyCircuitDepth = False

    modifyCircuitDepth = False

    addAdditionalFeature = False

    addAdditionalInputsAndOutputs = False

    useTrainedModel= False

    useNoise= False

    modelName = 'svm00'
    
    allDataTypes=['Wine Data', 'Load Digits', 'Credit Card', 'MNIST', 'Make Classification']

    featureMaps=['Amplitude Embedding', 'Angle Embedding', 'Custom Embedding']

    # savingFileName = 'my_dataframe.csv'

    # savingFileName = 'my_dataframe_noisy1.csv'

    savingFileName = 'my_dataframe_no_noise.csv'

    # savedModelsFolder = 'saved_models'

    # savedModelsFolder = 'saved_models_noisy1'

    #first naming
    # savedModelsFolder = 'saved_models_all_extra_extra_noise_data11'

    #second naming
    savedModelsFolder = 'saved_models_all/noise1_95_2_95_3_95_4_95_data_1'

    useQiskit = False

    #noise 1
    applyDepolarizingChannelNoise = False

    depolarizingChannelNoise = 0.5

    #noise 2
    applyAfterEnganglementNoise = False

    afterEnganglementNoise = 0.5

    #noise 3
    applyBitFlipNoise = False

    bitFlipNoise = 0.9
    # bitFlipNoise = 0.5

    #noise 4
    applyAmplitudeDampingNoise = False
    
    amplitudeDampingNoise = 0.5

    #noise 5
    applyPhaseDampingNoise = False

    phaseDampingNoise = 0.5

    doOneKfold = True
    
    onlyKFoldValue = 0

    doOneScalar = False

    onlyScalarValue = 3

    usePercentageOfData = True

    PercentageOfData = 0.01

    testMutation = 0

    # Mutants 1-30; Sept-style: amplitude uses 1-10, angle uses 11-30 (disjoint)
    mainClassMutationList = [14, 17]

    mainStatisticalClassMutationList = [18, 21]

    dataMutationList = [15]

    metamorphicMutationList = [19]

    featureMapMutationList = [1, 2, 3, 4, 5, 6, 11, 12, 13, 16, 20, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    
    featureMapMutationListOrganized = [1, 2, 3, 4, 5, 6]

    qKernelMutationList = [7, 8, 9, 10]

    mutantTypes = ['Equivalent', 'Killed', 'Survived', 'Crashed']

    allQMLDevicesTypes = [
        'default.qubit',
        'lightning.qubit',
        'default.mixed',
        # 'qiskit.aer',
        # 'qiskit.basicsim',
        # 'qiskit.remote',
    ]

    selectedQMLDeviceType = 1

    allOptimizationLevels = [0,1,2]

    selectedOptimizationLevel = 1

    def getModelName(mrNumber, mrValue, fold_index, n_folds):

        return 'SVM'+ str(0) + str(mrNumber)+ '-' + str(mrValue) + '-' + str(fold_index) + '-of-' + str(n_folds)

    def getFullPathModelName(modelName):

        return f'saved_models/{modelName}'


   