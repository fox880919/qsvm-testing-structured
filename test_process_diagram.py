#!/usr/bin/env python3
"""
Generate a visual flowchart of the QSVM Structure Testing process.
Produces: test_process_diagram.png (or .svg) and test_process_diagram.md (Mermaid).

Run: python test_process_diagram.py
View Mermaid: Open test_process_diagram.md in VS Code or paste at https://mermaid.live
"""

import os
import sys

# Try graphviz first (best quality), then matplotlib (fallback), else just Mermaid
USE_GRAPHVIZ = False
USE_MATPLOTLIB = False

try:
    import graphviz
    USE_GRAPHVIZ = True
except ImportError:
    pass

if not USE_GRAPHVIZ:
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
        USE_MATPLOTLIB = True
    except ImportError:
        pass


def save_mermaid():
    """Save Mermaid diagram (always works, view at mermaid.live or in VS Code)."""
    mermaid = '''
# QSVM Structure Testing - Visual Process Diagram
Open this file in VS Code (Mermaid extension) or paste the code block at https://mermaid.live

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
'''
    out_path = os.path.join(os.path.dirname(__file__), "test_process_diagram.md")
    with open(out_path, "w") as f:
        f.write(mermaid)
    print(f"  Mermaid saved: {out_path}")
    return out_path


def build_graphviz_diagram():
    """Build diagram using graphviz."""
    dot = graphviz.Digraph(comment="QSVM Test Process", format="png")
    dot.attr(rankdir="TB", splines="ortho", nodesep="0.4", ranksep="0.5")
    dot.attr("node", shape="box", style="rounded,filled", fontname="Helvetica")
    dot.attr("edge", fontname="Helvetica")

    # Main flow
    dot.node("start", "Start", fillcolor="#e1f5fe")
    dot.node("loop", "for i in range(1, 13)\nMRs 1-12", fillcolor="#fff3e0")
    dot.node("r0", "runLoop(0,i)\nAmplitude", fillcolor="#e8f5e9")
    dot.node("r1", "runLoop(1,i)\nAngle", fillcolor="#e8f5e9")
    dot.node("ang", "Mutants 1-10", fillcolor="#f3e5f5")
    dot.node("amp", "Mutants 11-30", fillcolor="#f3e5f5")
    dot.node("run", "runScript", fillcolor="#fce4ec")
    dot.node("orig", "Original run\n(mutant 0)", fillcolor="#fff8e1")
    dot.node("mut", "For each mutant:\nLoad & Execute", fillcolor="#fff8e1")
    dot.node("eq", "Equivalent", fillcolor="#c8e6c9")
    dot.node("diff", "Different score", fillcolor="#ffccbc")
    dot.node("stat", "Statistical Test\nt-test, p<0.05", fillcolor="#b2dfdb")
    dot.node("kill", "Killed", fillcolor="#c8e6c9")
    dot.node("surv", "Survived", fillcolor="#ffccbc")
    dot.node("save", "saveToDataFrame", fillcolor="#e0e0e0")
    dot.node("omni", "run_step2_kernel_test", fillcolor="#e1f5fe")
    dot.node("data", "Wine Data\n3 encodings", fillcolor="#e3f2fd")
    dot.node("defects", "5 defects\ncombinations", fillcolor="#f3e5f5")
    dot.node("qnode", "qnode_omni\nKernel only", fillcolor="#e8eaf6")
    dot.node("mr14", "14 MRs check", fillcolor="#fff3e0")
    dot.node("csv", "results CSV", fillcolor="#e0e0e0")

    dot.edge("start", "loop")
    dot.edge("loop", "r0")
    dot.edge("loop", "r1")
    dot.edge("r0", "ang")
    dot.edge("r1", "amp")
    dot.edge("ang", "run")
    dot.edge("amp", "run")
    dot.edge("run", "orig")
    dot.edge("orig", "mut")
    dot.edge("mut", "eq")
    dot.edge("mut", "diff")
    dot.edge("diff", "stat")
    dot.edge("stat", "kill")
    dot.edge("stat", "surv")
    dot.edge("eq", "save")
    dot.edge("kill", "save")
    dot.edge("surv", "save")
    dot.edge("save", "loop")
    dot.edge("loop", "omni")
    dot.edge("omni", "data")
    dot.edge("data", "defects")
    dot.edge("defects", "qnode")
    dot.edge("qnode", "mr14")
    dot.edge("mr14", "csv")

    return dot


def build_matplotlib_diagram():
    """Build diagram using matplotlib."""
    fig, ax = plt.subplots(1, 1, figsize=(14, 18))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 24)
    ax.axis("off")

    def box(x, y, w, h, text, color="#e3f2fd"):
        p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02", 
                           facecolor=color, edgecolor="#37474f", linewidth=1)
        ax.add_patch(p)
        ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=7, wrap=True)

    def arrow(x1, y1, x2, y2):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="#455a64", lw=1.5))

    # Rows from top
    row = 22
    box(4, row, 2, 0.6, "Start", "#e1f5fe")
    row -= 1.2
    box(3.5, row, 3, 0.6, "for i in range(1,13) - MRs 1-12", "#fff3e0")
    row -= 1.5
    box(2, row, 2.2, 0.8, "runLoop(0,i)\nAngle", "#e8f5e9")
    box(5.8, row, 2.2, 0.8, "runLoop(1,i)\nAmplitude", "#e8f5e9")
    row -= 1.2
    box(2, row, 2.2, 0.5, "Mutants 1-6", "#f3e5f5")
    box(5.8, row, 2.2, 0.5, "Mutants 1-30", "#f3e5f5")
    row -= 1.2
    box(4, row, 2, 0.6, "runScript", "#fce4ec")
    row -= 1.2
    box(4, row, 2, 0.6, "Original + Mutants", "#fff8e1")
    row -= 1.2
    box(2, row, 2, 0.5, "Equivalent", "#c8e6c9")
    box(4, row, 2, 0.5, "Different", "#ffccbc")
    box(6, row, 2, 0.5, "Crashed", "#ffcdd2")
    row -= 1.2
    box(4, row, 2.5, 0.6, "Statistical Test\nK-fold, t-test", "#b2dfdb")
    row -= 1.2
    box(3, row, 2, 0.5, "Killed", "#c8e6c9")
    box(5, row, 2, 0.5, "Survived", "#ffccbc")
    row -= 1.2
    box(4, row, 2, 0.5, "saveToDataFrame", "#e0e0e0")
    row -= 1.5
    box(4, row, 2.5, 0.6, "Step 2: Kernel Testing", "#e1f5fe")
    row -= 1.2
    box(4, row, 2.5, 0.5, "Wine Data, 3 encodings", "#e3f2fd")
    row -= 1
    box(4, row, 2.5, 0.5, "5 defects combinations", "#f3e5f5")
    row -= 1
    box(4, row, 2.5, 0.5, "Kernel only", "#e8eaf6")
    row -= 1
    box(4, row, 2.5, 0.5, "14 MRs check", "#fff3e0")
    row -= 1
    box(4, row, 2, 0.5, "results CSV", "#e0e0e0")

    # Arrows
    arrow(5, 22, 5, 21.4)
    arrow(5, 20.8, 5, 20.2)
    arrow(3.1, 19.6, 3.5, 19)
    arrow(6.9, 19.6, 6.5, 19)
    arrow(3.1, 18.4, 4, 17.8)
    arrow(6.9, 18.4, 6, 17.8)
    arrow(5, 17.2, 5, 16.6)
    arrow(5, 15.4, 5, 14.8)
    arrow(5, 13.6, 5, 12.4)
    arrow(5, 11.2, 5, 10.6)
    arrow(5, 9.4, 5, 8.8)
    arrow(5, 7.6, 5, 6.6)
    arrow(5, 5.4, 5, 4.8)
    arrow(5, 3.6, 5, 3)
    arrow(5, 2.4, 5, 1.9)

    plt.tight_layout()
    return fig


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    print("QSVM Test Process - Diagram Generator")
    print("-" * 40)

    # Always save Mermaid
    save_mermaid()

    # Try graphviz
    if USE_GRAPHVIZ:
        try:
            dot = build_graphviz_diagram()
            out_path = os.path.join(script_dir, "test_process_diagram")
            dot.render(out_path, cleanup=True)
            print(f"  PNG saved: {out_path}.png")
        except Exception as e:
            print(f"  Graphviz render failed: {e}")
            print("  Use test_process_diagram.md with Mermaid instead.")

    # Fallback to matplotlib
    elif USE_MATPLOTLIB:
        try:
            fig = build_matplotlib_diagram()
            out_path = os.path.join(script_dir, "test_process_diagram.png")
            fig.savefig(out_path, dpi=120, bbox_inches="tight")
            plt.close()
            print(f"  PNG saved: {out_path}")
        except Exception as e:
            print(f"  Matplotlib failed: {e}")
            print("  Use test_process_diagram.md with Mermaid instead.")

    else:
        print("  Install graphviz (pip install graphviz) or matplotlib for PNG output.")
        print("  View test_process_diagram.md at https://mermaid.live")

    print("-" * 40)
    print("Done. Open test_process_diagram.md or .png to view.")


if __name__ == "__main__":
    main()
