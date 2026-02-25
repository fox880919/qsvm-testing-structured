# QSVM Structure Testing - Visual Process Diagram

**View options:** Open in VS Code (Mermaid extension) or paste a code block at https://mermaid.live

---

## Simplified Flow (recommended for quick view)

```mermaid
flowchart TB
    A([Start]) --> B[for i = 1 to 12: MRs]
    B --> C[Set MR flags 6-12]
    C --> D[Amplitude: Mutants 1-10]
    C --> E[Angle: Mutants 11-30]
    D --> F[runScript]
    E --> F
    F --> G[Original score]
    G --> H[For each mutant]
    H --> I{Score vs Original?}
    I -->|Same| J[Equivalent]
    I -->|Different| K[Statistical t-test]
    I -->|Exception| L[Crashed]
    K -->|p<0.05| M[Killed]
    K -->|p≥0.05| N[Survived]
    J --> O[saveToDataFrame]
    M --> O
    N --> O
    L --> O
    O --> B
    B --> P[Step 2: Kernel Testing]
    P --> Q[Wine Data → 3 encodings]
    Q --> R[5 defects × combos]
    R --> S[qnode_omni kernel]
    S --> T[14 MRs check]
    T --> U[results CSV]
```

---

## Full Diagram (with subgraphs)

```mermaid
flowchart TB
    subgraph MAIN["main.py - Entry"]
        START([Start])
        LOOP["for i in range(1, 13)<br/>MRs 1-12"]
    end

    subgraph MRFLAGS["MR-Specific Flags"]
        MR6["MR6: addQuantumRegister"]
        MR7["MR7: injectNullEffect"]
        MR8["MR8: injectParameter"]
        MR9["MR9: changeDevice"]
        MR10["MR10: changeOptimization"]
        MR11["MR11: reverseWires"]
        MR12["MR12: reverseQubitsMult"]
    end

    subgraph STEP1["STEP 1: Mutation Testing"]
        R0["runLoopThroughAllTests(0, i)"]
        R1["runLoopThroughAllTests(1, i)"]
        
        subgraph AMP["Amplitude Embedding"]
            A_MUT["Mutants 1-10<br/>(Sept-style)"]
        end
        
        subgraph ANGLE["Angle Embedding"]
            B_MUT["Mutants 11-30<br/>(Sept-style)"]
        end
        
        RUN["runScript(mrNumber, mrValue)"]
        ORIG["Run Original (mutant 0)"]
        MUT["For each mutant: Load & run"]
        
        subgraph CLASS["Classify Result"]
            EQ["Equivalent<br/>score unchanged"]
            DIFF["Different score"]
            CRASH["Crashed"]
        end
        
        STAT["Statistical Test<br/>MainStatisticalClass.runTest<br/>K-fold, t-test"]
        KILL["Killed: p < 0.05"]
        SURV["Survived: p >= 0.05"]
        SAVE["saveToDataFrame"]
    end

    subgraph STEP2["STEP 2: Kernel Testing"]
        OMNI["run_step2_kernel_test()"]
        DATA["Load Wine → PCA → 3 encodings<br/>basis, angle, amplitude"]
        DEFECTS["5 defects: superposition, entanglement<br/>gate_error, swap_topology, param_noise"]
        MUTATOR["AutoMutator.apply_feature_map"]
        QNODE["qnode_omni: K(x1,x2) via FM + adjoint"]
        MRS14["Check 14 Metamorphic Relations"]
        CSV["results_v41_kernel_test.csv"]
    end

    subgraph MANAGERS["Dynamic Loading (per mutant)"]
        FM["FeatureMapManager"]
        QK["QKernelManager"]
        MC["MainClassManager"]
        MSC["MainStatisticalClassManager"]
        DM["DataManager"]
        META["MetamorphicRelationsManager"]
    end

    subgraph MUTANTS["30 Mutants by Subsystem"]
        FM_M["1-6,11-13,16,20,22-30: Feature Map"]
        QK_M["7-10: Quantum Kernel"]
        MC_M["14,17: MainClass"]
        MSC_M["18,21: Statistical"]
        DM_M["15: Data"]
        META_M["19: Metamorphic"]
    end

    START --> LOOP
    LOOP --> MRFLAGS
    MRFLAGS --> R0
    MRFLAGS --> R1
    R0 --> A_MUT
    R1 --> B_MUT
    A_MUT --> RUN
    B_MUT --> RUN
    RUN --> ORIG
    ORIG --> MUT
    MUT --> CLASS
    CLASS --> EQ
    CLASS --> DIFF
    CLASS --> CRASH
    DIFF --> STAT
    STAT --> KILL
    STAT --> SURV
    EQ --> SAVE
    KILL --> SAVE
    SURV --> SAVE
    CRASH --> SAVE
    SAVE --> LOOP
    LOOP --> OMNI
    OMNI --> DATA
    DATA --> DEFECTS
    DEFECTS --> MUTATOR
    MUTATOR --> QNODE
    QNODE --> MRS14
    MRS14 --> CSV
    MUT -.-> MANAGERS
    MANAGERS -.-> MUTANTS
```
