/**
 * Site copy — edit this file to change all text on the website.
 * All UI strings are centralized here for easy customization.
 */

import { DEFAULT_NOTEBOOK_SECTIONS, DEFAULT_NOTEBOOK_TABS } from "./notebookData"

export const SITE_COPY = {
  // Page title (also set in index.html)
  pageTitle: "QSVM Structure Testing | King's College London",

  // Header
  header: {
    title: "QSVM Structure Testing",
    subtitle: "Mutation, Metamorphic & Statistical Testing",
    logoAlt: "King's College London",
    tabs: {
      home: "Home",
      experiment: "Experiment",
      notebook: "Notebook",
      report: "Report",
    },
  },

  // Footer
  footer: "King's College London — QSVM Testing: Metamorphic, Mutation, Statistical & Quantum Kernel",

  // Home page
  home: {
    introTitle: "Introduction",
    introPara1:
      "This website presents a comprehensive testing framework for Quantum Support Vector Machines (QSVM) that combines metamorphic testing, mutation analysis, and statistical testing with dedicated quantum kernel testing including golden matrix evaluation.",
    introPara2:
      "The framework executes a two-step pipeline. Step 1 applies metamorphic relations across 30 mutants with angle and amplitude embeddings, using statistical t-tests (p < 0.05) to classify mutants as Equivalent, Killed, Survived, or Crashed. Step 2 isolates the quantum kernel with 3 feature maps (basis, angle, amplitude), 5 defect types, 14 metamorphic relations, and golden matrix comparison for kernel validation.",
    introPara3:
      "Use the Experiment tab to configure and run the tests. The Notebook and Report sections will provide additional documentation and analysis.",
    studentTitle: "Student",
    supervisorsTitle: "Supervisors",
  },

  // Experiment page
  experiment: {
    configTitle: "Configuration",
    datasetLabel: "Dataset",
    runLabel: "Run",
    kfoldLabel: "K-fold (Exp 1 & 2)",
    runButton: "Run Tests",
    runningButton: "Running...",
    cancelButton: "Cancel",
    liveProgressTitle: "Live Progress",
    runOutputTitle: "Run Output",
    downloadStep1: "Download Statistical Testing CSV",
    downloadStep2: "Download Kernel Testing CSV",
    datasetOptions: {
      0: "Wine",
      1: "Load Digits",
      2: "Credit Card",
      3: "MNIST",
    },
    experimentOptions: {
      all: "All (Baseline + Statistical Testing + Kernel Testing)",
      "1": "Baseline only",
      "2": "Statistical Testing only",
      "3": "Kernel Testing only",
    },
    phases: [
      {
        id: "config",
        title: "Configuration",
        description:
          "Dataset and K-fold values are set. The pipeline will use these for loading data and cross-validation.",
      },
      {
        id: "step1",
        title: "Baseline",
        description:
          "MR#1 (scaling) and MR#2 (rotation) on data. No mutations. Checks MTS=0 to verify QSVM determinism.",
      },
      {
        id: "step2",
        title: "Statistical Testing",
        description:
          "Full QSVM pipeline: 30 mutants, 12 metamorphic relations, amplitude + angle embeddings. Statistical t-test (p < 0.05) determines Equivalent, Killed, Survived, or Crashed.",
      },
      {
        id: "step3",
        title: "Kernel Testing",
        description:
          "Quantum kernel only: 3 feature maps (basis, angle, amplitude), 5 defects, 14 metamorphic relations. Golden matrix comparison for kernel validation. No full QSVM—kernel-level testing.",
      },
      {
        id: "done",
        title: "Results",
        description: "Download Statistical Testing and Kernel Testing CSV results.",
      },
    ],
    vizOnlyWine: "Visualization only available for Wine dataset",
    pipelineTitle: "Experiment Pipeline Visualization",
    pipelineDesc: "Data extraction → PCA → Feature map circuits → Training → Accuracy → Mutation analysis → Golden matrix & kernel testing.",
    vizTitle: "QSVM Live Visualization",
    vizDesc: "Decision boundary and data classification (2D PCA projection). Generate during or after the experiment.",
    vizGenerating: "Generating...",
    vizAmplitude: "Amplitude Embedding",
    vizAngle: "Angle Embedding",
    vizSwitchWine: "Switch to Wine dataset to enable visualization.",
    vizAlt: "QSVM decision boundary",
    phasesTitle: "Testing Phases",
    resultsTitle: "Results",
    runCancelled: "Run cancelled.",
    runFailed: "Tests failed. Check the run output below.",
    starting: "Starting...",
  },
  pipeline: {
    overviewTitle: "Experiment Pipeline Overview",
    generateFigures: "Generate report figures",
    generateFiguresRunning: "Generating...",
    runAfterHint: "Run after Experiments 2 or 3 to create heatmaps and charts.",
    exp1Title: "Baseline",
    exp1Desc: "MR1 (scaling) and MR2 (rotation) on data, no mutations. MTS=0 check for baseline consistency.",
    exp1NoFigures: "Run Baseline to verify behavior. No report figures for this experiment.",
    exp2Title: "Statistical Testing",
    exp2Desc: "30 mutants, 12 metamorphic relations, amplitude + angle embeddings. Statistical t-test (p < 0.05) for Killed/Survived.",
    dataExtraction: "1. Data Extraction",
    dataset: "Dataset",
    samples: "Samples",
    featuresRaw: "Features (raw)",
    classes: "Classes",
    pcaTitle: "2. PCA (if applicable)",
    pcaNotApplied: "PCA not applied. Using raw features.",
    featureMapTitle: "3. Feature Map Circuits",
    amplitudeEmbedding: "Amplitude Embedding",
    angleEmbedding: "Angle Embedding",
    qsvmTraining: "4. QSVM Training",
    qsvmTrainingDesc: "Kernel matrix computation → SVM (precomputed kernel) → Accuracy via train/test split. See QSVM Live Visualization above for decision boundary.",
    mutationResults: "5. Mutation Analysis Results",
    runTestsForExp2: "Run tests to see Statistical Testing results (mutation analysis).",
    reportFigures: "Report Figures",
    mutantHeatmap: "Mutant Outcome Heatmap",
    detectionCoverage: "Detection Coverage",
    exp3Title: "Kernel Testing",
    exp3Desc: "Quantum kernel only: 3 feature maps (basis, angle, amplitude), 5 defects, 14 metamorphic relations. No full QSVM—kernel-level validation.",
    goldenMatrixTitle: "Golden Matrix & Kernel Testing Results",
    goldenMatrixDesc: "Mode × Defect combos, Caught_Rate per MR. 3 feature maps (basis, angle, amplitude), 14 MRs.",
    mode: "Mode",
    defects: "Defects",
    caughtRate: "Caught_Rate",
    runTestsForExp3: "Run tests to see Kernel Testing results (Golden matrix & kernel testing).",
    statisticalDetection: "Statistical Detection Confidence",
    mrEfficiency: "MR Efficiency Heatmap",
    loadingPipeline: "Loading pipeline visualization...",
  },
  notebook: {
    title: "Interactive Notebook",
    intro: "Explore the QSVM testing framework. Navigate between subsections below. Click Run on any code cell.",
    tabs: DEFAULT_NOTEBOOK_TABS,
    sections: DEFAULT_NOTEBOOK_SECTIONS,
  },
  headerFallback: {
    kings: "KING'S",
    college: "College ",
    london: "LONDON",
  },

  // Report page
  report: {
    title: "Progress Report — LaTeX Source",
    description: "Edit the LaTeX source below. Click Save & Recompile to update the PDF.",
    saveButton: "Save & Recompile PDF",
    savingButton: "Saving & Compiling…",
    viewPdfButton: "View PDF",
    saveSuccessMessage: "Saved and PDF updated successfully.",
    loadingText: "Loading…",
    fileNotFound: "progress_report_8.tex not found.",
  },

  // Project info (student & supervisors)
  project: {
    student: {
      name: "Faiez Altamimi",
    },
    supervisors: [
      { name: "Prof. Mohammad Mousavi", role: "Primary Supervisor" },
      { name: "Dr. Gunel Jahangirova", role: "Secondary Supervisor" },
    ],
  },
} as const
