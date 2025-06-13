# bellman-viterbi
# Burst Detection with Viterbi and Trellis Algorithms

This tool detects bursts in sequences of message offsets (time gaps between events) using two algorithms:
- **Viterbi-based burst detection**, based on Kleinberg's model.
- **Trellis-based dynamic programming** (Bellman-Ford inspired).

## 🔍 Purpose

To analyze timestamped events (e.g. messages, posts) and identify periods of increased activity (bursts).

## 📥 Input

A plain text file with space-separated time intervals (offsets), like:
