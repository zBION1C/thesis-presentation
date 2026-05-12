---
theme: academic 
layout: cover 
hideInToc: true
colorSchema: light
transition: slide-left 
coverDate: false
highlighter: shiki
fonts:
    mono: "Fira Code"
---

## Spotting Accuracy Issues in Profile-Guided Optimization 
A new methodology to spot metadata propagation errors within optimization pipelines

<div class="flex items-center" style="gap:50px">
<span>
Supervisor<br>
Prof. Daniele Cono D'Elia
</span>
<span>
Co-supervisor<br>
Dr. Cristian Assaiante
</span>
</div>

<div class="absolute bottom-0 right-0">
    <img src="/images/logo.png" width="300" height="300">
</div>

---
hideInToc: true
---
# Table of Contents
<Toc maxDepth=1 />

---
layout: figure-side
figureUrl: "/images/compiler_structure.svg"
---

# Compilers 

<v-clicks every="1">

- What is a compiler?
    - Translates source code -> target code
    - Preserves program semantic
    - *Optimizes* code during translation
- Compiler Structure (3 Stages)
    - Front-end -> Parses source code -> builds IR
    - Middle-end -> Optimizes IR
    - Back-end -> Generates target code
- Intermediate Representation (IR)
    - Multiple IR types exist
    - Depends on compiler design goals

</v-clicks>

---

# Optimizations

- The optimization process
    - A sequence of transformations (a.k.a. Pipeline)
    - The IR is processed at each pass 
    - Output is a *better* program w.r.t. some performance metrics.
    - Supported by static or dynamic analysis that <span v-mark="{at:1, color: 'red', type: 'underline'}">estimate</span> control-flow

<br>
<br>
<br>
<div align="flex flex-col items-center"> 
    <img src="./images/pipeline.svg" class="mx-auto">
</div>

---

# Profile Guided Optimization

<v-clicks every="1">

- A smart optimization technique
    - Leverages *control flow information* captured at runtime to steer optimizations
    - Notable performance improvement 
- Control flow information (or *profile*) a.k.a. 
    - Weights on control flow edges
    - Counts on basic blocks
- Profiles can be captured via:
    - Instrumentation -> Additional logic inside the program
    - Sampling -> CPU counters + Perf
    - Tracing -> Profile aggregated from the program trace 

</v-clicks>

---
layout: image
image: "/images/pgo.svg"
backgroundSize: 80%
---
## <span class="text-black">PGO Workflow</span>
---
layout: figure-side
figureUrl: "/images/llvm.svg"
figureCaption: "LLVM architecture"
---

# The LLVM Project

- The LLVM Project 
    - A collection of modular and reusable compiler and toolchain technologies
    - Designed around a modern SSA-based compilation strategy 

<v-clicks depth="1">

- Key Components
    - LLVM Core -> Source- and target-independent optimizer
    - Clang -> Native C/C++ compiler for LLVM
    - LLD ->  High-performance linker

</v-clicks>

<v-click>

...and many more!

</v-click>

---

# Profile Guided Optimization in LLVM 

- Profile information encoded as instruction metadata
    - `branch_weights` -> Counts associated to instructions that change the control flow 
    ```llvm {all|4,5}
    bb41:
      store i32 0, ptr %i40, align 4
      %i42 = load <4 x i32>, ptr @h, align 16
      br i1 %i39, label %.split.us.preheader, label %.split.preheader, !prof !30
    !30 = !{!"branch_weights", i32 2000, i32 1000}
    ```
    - `function_entry_counts` -> Number of times a function was called
    ```llvm {all|4}
    define i32 @foo() !prof !1 {
      ret i32 0
    }
    !1 = !{!"function_entry_count", i64 2590}
    ```
    - `vp` -> Profiles data values passed to functions (Not treated)

---

## Control Flow Analysis

- Profile metadata used to compute additional control flow data

    - `BranchProbabilityInfo` -> Raw branch weights converted into branch probabilities
    - `BlockFrequencyInfo` -> Blocks are assigned an execution frequency relative to the entry block 
    - `ProfileSummaryInfo` -> Hotness or coldness of blocks 

<div class="flex" style="height:55%;align-items:center;justify-content:center;gap:10px;">
<div style="flex:1;"> 

```llvm 
entry:
  %cmp = icmp sgt i32 %x, 0
  br i1 %cmp, label %then, label %else, !prof !0

then:
  ret i32 1

else:
  ret i32 0

!0 = !{!"branch_weights", i32 80, i32 20}
!1 = !{!"function_entry_count", i64 1000}
```

</div>
<div style="flex:1; display:flex; flex-direction:column; gap:10px;">
<div style="flex:1;"> 

BranchProbInfo
```llvm 
edge %entry -> %then probability is 0x66666666 / 0x80000000 = 80.00%
edge %entry -> %else probability is 0x1999999a / 0x80000000 = 20.00%
```

</div>
<div style="flex:1;">

BlockFrequencyInfo
```llvm
then: float = 0.8, int = 14411518804230144, count = 800
else: float = 0.2, int = 3602879705251840, count = 200
```

</div>
</div>
</div>

---

# Profile Information Propagation 

- The starting profile is propagated throughout the entire pipeline
    - Each LLVM optimization is responsible for the update of the profile information
    - Additional logic to handle profile metadata in passes source code

<div class="p-20px" align=center>
    <img src="/images/propagation.svg">
</div>

- Bugs in such a logic reduce the efficacy of PGO
    - Subsequent pass will work on wrong profile information
    - A cascading effect will trigger
    - Bad optimization decisions can be taken!

---

# Problem Formalization

<div class="flex flex-col" style="justify-content:center;height:90%">
<DefinitionBox title="Definition 3: Profile propagation analysis problem">

Let $O$ be a profile-guided optimization pipeline. Let $(G, p)$ be a profiled program. Let $(G', p') = O(G, p)$ be the profiled program resulting by applying $O$ to $(G, p)$.
The *profile propagation analysis problem* consist of performing the following tasks:
- Determine if $O$ made some profile propagation errors.
- If profile propagation errors were made by $O$, spot the faulty passes for this errors.

</DefinitionBox>
</div>

---

## Profile and Block Frequency Formalization

<div class="flex flex-col" style="justify-content:center;height:90%;gap:10px">
<DefinitionBox title="Definition 1: Profiled Program">

Given a program $A$ represented as a control-flow graph $G=(E,V)$, a *profile* of $A$ is a function $p: E \to \mathcal{N}$
that assigns to each edge $(v,w) \in G$ the number of times control flows from basic block $v$ to basic block $w$.
We denote the program $A$ with profile $p$ as the pair $(A,p)$.

</DefinitionBox>

<DefinitionBox title="Definition 2: Block Frequency">

Give a profiled program $(G=(V,E), p)$ the *block frequency function* is a function $f_p: V \to \mathcal{N}$ that assigns to each basic block
$v \in V$ the number of times $v$ is reached during program execution, as derived from profile $p$.

</DefinitionBox>
</div>

---

## Spotting profile propagation errors 

<DefinitionBox title="Definition 4: Profile Equivalence Relation">

Let $p$ and $q$ be two profiles for the same program $G$ and let $f_p$ and $f_q$ be their respective block frequency functions.
$p$ is said to be equivalent to $q$ if $\forall v \in V, f_p(v) = f_q(v)$ 

</DefinitionBox>

<v-clicks :depth=2>

- Now consider:
    - $p$ -> profile computed by the pipeline on the optimized program
    - $q$ -> profile computed instrumenting and re-executing the optimized program 
    - if $p \neq q$ then pipeline made some profile propagation errors 

</v-clicks>

---

## Identifying Culprit Passes 


<DefinitionBox title="Definition 5: Profile Mismatch">

Let $p$ and $q$ be two profiles for the same program $G$ and let $f_p$ and $f_q$ be their respective block frequency functions.
Let $p\neq q$.<br> A *profile mismatch* is a tuple $(G, f, bb, f_p(bb), f_q(bb))$ such that
- $f$ is a function within $G$
- $bb$ is a basic block within $f$ 
- $f_p(bb) \neq f_q(bb)$

</DefinitionBox>

<v-clicks>

- A single pipeline application can results in multiple profile mismatches 
- We need a way to attribute to a mismatch the pass that caused it...

</v-clicks>

---
hideInToc: true
---

## Identifying Culprit Passes

<DefinitionBox title="Definition 6: Mismatch Equivalence Relation">

Let $G$ and $G'$ be programs, where $G'$ is obtained by manipulating $G$ in some way.
Let $m_1 = (G, f, bb, f_p(bb), f_q(bb))$ and $m_2 = (G', f', bb', f_p(bb'), f_q(bb'))$ be two mismatches for their respective programs.
Then $m_1 = m_2$ if
- $f$ and $f'$ names are equal
- $f_p(bb) = f_p(bb')$ 
- $f_q(bb) = f_q(bb')$

</DefinitionBox>

<div align=center style="height:100%" v-click v-motion :initial="{x:-50}" :enter="{x:0}" >
<img src="/images/method.svg">
</div>

---
layout: image
image: "/images/opt_phase.svg"
backgroundSize: 60%
---

# <span class="text-black">Optimization Phase</span>

---
layout: image
image: "/images/search.svg"
backgroundSize: 60%
---

# <span class="text-black">Search Phase</span>

---

# Results

- Eight major fuzzing campaigns were launched varying on
    - Optimization pipelines tested
    - Program generations parameters
    - Globally disabled passes
- Eleven total issues were found and reported to the LLVM community

<div align=center>
<img src="/images/table.png" width=40% />
</div>
