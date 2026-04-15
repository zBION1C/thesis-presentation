---
theme: academic 
layout: cover 
hideInToc: true
colorSchema: light
transition: slide-left 
coverDate: false
fonts:
    sans: "Firacode"
    fallbacks: false
---

## Profile Information Propagation Analysis
A new methodology to spot metadata propagation errors within optimization pipelines

<div class="flex items-center" style="gap:50px">
<span>
Supervisor<br>
Prof. Daniele Cono D'Elia
</span>
<span>
Co-supervisor<br>
PhD. Cristian Assaiante
</span>
</div>

<div class="absolute bottom-0 right-0">
    <img src="./static/logo.png" width="300" height="300">
</div>

---
hideInToc: true
---
# Table of Contents
<Toc :columns="2"/>

---
layout: figure-side
figureUrl: "./static/compiler_structure.svg"
---

# What is a compiler? 
- Translates source code -> target code
- Preserves program semantic
- **Optimizes** code during translation

Compiler Structure (3 Stages)

- Front-end → Parses source code → builds IR
- Middle-end → Optimizes IR
- Back-end → Generates target code

Intermediate Representation (IR)

- Multiple IR types exist
- Choice depends on compiler design goals


---
layout: figure-side
figureUrl: "./static/llvm.svg"
figureCaption: "LLVM Architecture"
---
## LLVM Compiler Infrastructure

The LLVM Project 
- A collection of modular and reusable compiler and toolchain technologies,
- Designed around a modern SSA-based compilation strategy that supports both static and dynamic compilation of arbitrary programming languages.

Key Components

- LLVM Core -> Source- and target-independent optimizer
- Clang -> Native C/C++ compiler for LLVM
- LLD ->  High-performance linker

...and many more!

---

# Profile Guided Optimization

---

## Workflow 

---

## Instrumentation

---

# Problem Formalization

---
layout: two-cols-header
---
# Proposed Methodology

::left::

<v-click>

### Optimization phase

</v-click>

::right::
<v-click>

### Search phase

</v-click>

---
layout: figure-side 
figureUrl: "./static/test.png"
figureCaption: "Optimization phase architecture"
---

## Optimization phase 

---

## Search phase

---

# Experimental Evaluation 

