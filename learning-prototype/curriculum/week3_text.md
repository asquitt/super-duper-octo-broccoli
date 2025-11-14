# Week 3: Text Topic Analysis

**Goal**: Extract topics, keywords, and important moments from transcripts.

---

## 📚 Learning Objectives

By the end of this week, you will:
- ✅ Understand basic NLP (Natural Language Processing)
- ✅ Extract keywords from text
- ✅ Detect topic changes
- ✅ Identify questions and answers
- ✅ Score text importance

---

## 🎯 What We're Building This Week

A text analyzer that can:
1. Parse transcripts (plain text, SRT, VTT)
2. Extract important keywords
3. Detect topic changes
4. Identify Q&A patterns
5. Score segments by importance

---

## 📖 Key Concepts

### 1. Text as Data

```
Transcript:
"Welcome to this amazing presentation about AI.
Today we'll explore machine learning basics.
First, let's understand neural networks.
Neural networks are inspired by the human brain."

Analysis:
- Keywords: AI, machine learning, neural networks, brain
- Topics: Introduction → ML Basics → Neural Networks
- Pattern: Question implied → Answer given
```

### 2. Keyword Extraction (TF-IDF)

**Term Frequency**: How often a word appears
**Document Frequency**: How many documents have this word
**TF-IDF**: Important words appear often but not everywhere

### 3. Topic Detection

Topics change when:
- New keywords appear
- Keyword overlap decreases
- Semantic similarity drops

### 4. Q&A Patterns

Questions:
- Start with "what", "how", "why", "when"
- End with "?"
- Usually followed by longer answer

---

## 💻 Starter Code

See `starter-code/week3_starter/text_analyzer.py`

---

## ✏️ Exercises

1. **Keyword Extraction**: Remove stop words, find frequent terms
2. **Topic Segmentation**: Split text when topics change
3. **Question Detection**: Identify all questions in transcript

---

## 🎯 Tasks

### Beginner
1. Parse plain text transcripts
2. Remove stop words
3. Count word frequency
4. Identify questions

### Intermediate
5. Calculate keyword density
6. Detect topic changes
7. Parse SRT/VTT format
8. Score segment importance

### Advanced
9. Use sentence embeddings (optional)
10. Implement semantic similarity
11. Detect topic hierarchies
12. Build Q&A matcher

---

**Next**: Week 4 - Visual Engagement Detection
