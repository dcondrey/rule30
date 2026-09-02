# Preregistration: two-ended holonomy-defect closure

## Discovery split

The frozen holonomy-closure audit through source length 10 showed:

- ordered `D8` defects plus their absolute rightmost phase are not closed;
- adding every scenario's previous endpoint is still not closed;
- complete reversed dependency queues are closed, as required by the exact
  queue recurrence.

An exploratory comparison on that same discovery corpus found no closure
collision after retaining both end symbols of every scenario queue.

## Held-out claim

For each active zero-prefix scenario at row `j`, augment the anchored defect
word by

```text
(first reversed-queue symbol, last reversed-queue symbol).
```

The first symbol is the currently exposed cut state and the last symbol is
the boundary image of the previous endpoint.  Freeze this exact depth-one,
two-ended annotation.  Test complete hard-core lengths beginning at 11.  A
shared annotated state with two different exact next-row defect words kills
transition closure.  No deeper window may be added to rescue this registered
state.

Passing finite lengths would establish only finite evidence for closure, not
an all-length transducer or an ordinal descent.
