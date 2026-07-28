# {name}

> one operation. that might be all you ever needed.

`{name}` is a minimal string-rewriting language built on a single primitive: **concat**. No arithmetic, no conditionals, no loops, no arrays. Everything else is expected to be built *from* concat — because concat, repeated, is enough.

```
name : d
{a.file}
```

That's a complete `{name}` program.

## Philosophy

`{name}` follows KISS — Keep It Simple, Stupid — taken to its limit: what is the single smallest operation a language can have, such that everything else stays reachable from it? The answer here is **concat with substitution** — take a name, replace it with its value, paste the result into the surrounding text. No keywords, no operators, no types beyond strings.

This sits in the same family as **semi-Thue systems** and **Markov algorithms**, where computing meant nothing more than rewriting a string until nothing changes. Conditionals, loops, arithmetic, arrays — none of them are primitives. They're libraries, written in `{name}` itself, out of concat.

## Getting Started

```bash
git clone https://github.com/sirnaser/name-lang.git
cd name-lang
python3 {name}.py
```

A `{name}` program conventionally looks like this:

```
main :

{code}

main : {main}
```

The first line resets `main` — a fresh slate, in the spirit of a `main` entry point. The last line does nothing functionally; it's a nod to `main` and to how little the language needs to mark an ending.

## Core Concepts

**Variables** are names bound to strings — the only value type there is.

**Assignment** binds a name: `answer : 42`

**Concat** is a reference to a variable, written `{name}`, replaced by its current value and pasted into place:
```
name : world
greeting : hello, {name}!
```
→ `greeting` is `"hello, world!"`. Change `name` to something else, and every future concat of `{name}` picks up the new value — there is no separate "recompute" step, this is just what concat does.

**`main`** silently accumulates the whole session as it runs. It exists so a program can export itself — write `{main}` to a file, and the entire program is on disk, ready to be loaded back in.

## Syntax

- **Assignment:** `name : value`
- **Block values:** a line ending in bare `:` opens a multi-line value, continued by lines indented with a tab or four spaces.
- **Bare expressions:** a line with no `:` is concatenated and re-run in place — this is how a file reference expands into a whole program that still executes top to bottom, in order.
- **Escaping:** `{-name}` is never a concat — the `-` protects it. Because of this, **variable names may never begin with `-`**.

Concat always resolves top to bottom, in program order: a later line always sees the *current* value of anything assigned above it — including values that just arrived from expanding a file reference a moment earlier.

## File I/O

Files are `{name}`'s entire I/O system:

- **Reading:** `{path.file}` splices a file's contents in as live source.
- **Writing:** an assignment whose name ends in `.file` writes the value to disk instead of storing a variable.

That's enough for a natural shape: **load** libraries from files, **run** the logic, **export** the result — or the program itself — back out. The `if`/`then`/`else` example below is exactly this shape: it *loads* input from `input.file`, *runs* the branching logic, and *exports* the answer to `output.file`.

## Conditionals, from nothing but concat

There is no `if` keyword in `{name}`. Here is one, built entirely out of concat — a complete, runnable program, not a fragment:

```
main :

if : 
    {-var}={{-var}} : {-else}
    {-var}={-val} : {-then}
    {{-var}={{-var}}}

name : {input.file}
var : name
val : naser

else :
    output.file : hello to the user of name-lang :)
then :
    output.file : hello to the creator of name-lang <3
{if}

main : {main}
```

The trick: `var=val` is built as a string two different ways — once with `val` substituted in literally, once with `{var}` substituted with its *real* value — and a dictionary lookup decides which branch was actually meant. If they land on the same key, `then` fires; otherwise, `else` does. Change what `input.file` contains, and `output.file` answers differently — no interpreter change required, because branching was never a primitive to begin with.

## Computational Power

`{name}`'s core mechanism places it in the same family as semi-Thue systems and Markov algorithms, both known to be Turing-complete. This is a strong, well-grounded conjecture for `{name}` too, not yet a proven fact — the plan is to prove it constructively, by encoding a Minsky machine purely in `{name}`.

## Roadmap

- [ ] Booleans and conditionals
- [ ] Loops
- [ ] Arithmetic
- [ ] Comparisons
- [ ] Arrays / lists
- [ ] A constructive Turing-completeness proof

## License

MIT

---

*One operation. That might be all you ever needed.*