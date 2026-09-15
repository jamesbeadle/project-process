# How I Write Code

Read this first. Everything below is how I think, not just what I want. If you understand the principle, the rules follow naturally. If you only follow the rules without the principle, you'll satisfy the letter and miss the point.

## The Core Idea

**Code is prose.** A file should read like a story about the domain. When someone reads it, they should understand what is happening without running it, without comments, and without holding much in their head. The language of the code — names, structure, flow — is how the domain reveals itself.

This is the lens. Every other rule below is a consequence of it.

**The diagnostic test:** if a line of code doesn't make sense as a sentence, something is wrong. Not with the line — with the structure around it. Bad code reads badly because it reflects a flawed understanding of the problem. When you feel friction reading, stop and restructure. Don't paper over it with a comment.

## How to Approach a Codebase

Before writing any code, the work has to flow through five stages in order. Each stage is derived from the one above it. Nothing exists in a lower stage that isn't demanded by a higher one.

**1. User stories.** A software project is the sum of its user stories. Every story has the shape *as X user, I want Y feature, for Z benefit*. If a feature can't be expressed this way, it shouldn't exist yet. The full set of stories defines the scope of the project — nothing more, nothing less.

**2. User experience through UI.** Each story is delivered through a view. Imagine the wireframe: what screens, what components, what flows. A table here, a form there, a modal for confirmation, a graph for the summary. The UI is the concrete realisation of the story. Industry-standard, high-quality UX — known patterns, known components, no invention for invention's sake.

**3. Site map.** Stories don't live in isolation and neither do their views. Map every story to a view, then map the views to each other — what links to what, what nests inside what, where the user enters, where they go next. A projects dashboard isn't a single-story view; it's a hub that fans out to every project-level feature. A project detail view serves dozens of stories at once. The site map consolidates the per-story wireframes into one coherent application.

What this reveals:
- **Shared views.** The same view appears in many stories. Design it once with full knowledge of every demand placed on it, not as a side-effect of one story at a time.
- **The navigation hierarchy.** Dashboard → project → task → comment isn't decoration, it's the user's mental model of the domain. If the navigation feels awkward, the domain hierarchy is wrong — fix the hierarchy, not the navigation.
- **Speculative views.** Any view not reached by a user story shouldn't exist. If you find one, either it's missing a story (go back to stage 1) or it's not needed (delete it).
- **Missing entry points.** Any story whose view isn't reachable through navigation has a gap — the user can never trigger it. Surface the gap before building anything.

**4. Data structure.** With a consolidated site map you now know every view and everything each view demands. The UI reveals the domain. A table's columns *are* an entity's properties. A form's fields *are* the inputs that entity accepts. A flag in the UI *is* a property on the model. Rarely does a domain property exist that doesn't surface somewhere in the UI — and when it does, it's derived from properties that do. Build the entity diagram from what the *unified* set of views demands across the whole site map. Single source of truth. Derive what's derivable; store what isn't.

**5. Backend.** By this point the hard decisions are made. Entities are known. Operations on them are known (because the UI demands them). The backend becomes a translation layer between the data structure and the UI, not a design problem. It articulates cleanly through CQRS — see below.

### The backend articulates through CQRS

CQRS is the default skeleton for the backend, chosen for the same reason everything else here is chosen: language. Every command and every query is a named intention that reads as a sentence — `CreateProject`, `ArchiveProject`, `GetProjectsForUser`. A command or query *is* a user story made executable. This maps the backend one-to-one onto the stories from stage 1, which is exactly the articulation the rest of these rules demand.

The flow within the backend:

1. **Every user story becomes a command or a query.** Commands change state; queries read it. If a story doesn't map cleanly to one or the other, the story isn't fully understood — go back up the chain. The full set of commands and queries should account for every story, nothing more.
2. **Implement the entry points with their gates.** Each command/query entry point handles authorisation, authentication, and validation *first* — before any domain logic runs. These are the gates the request passes through, and they read as exactly that.
3. **Identify the design pattern from expected usage.** Only now, knowing what the operations are and how heavily each will be used, does a scalable pattern reveal itself. This is emergent, not imposed — the same rule as everywhere else. Don't pick a pattern from a catalogue; let expected usage show you the shape.
4. **Wire the pattern implementations to the entry points.** The entry points (with their gates) delegate to the implementations the pattern produced.
5. **Derive types and DTOs from the implementations.** The data-transfer objects fall out of what the implementations actually need — they're discovered, not designed upfront. This is the same principle as entities falling out of the UI: the lower artefact is shaped by the demand above it, never speculated.

The discipline is that CQRS is the *framework for articulation*, not a constraint to fight. The design patterns that emerge inside it (step 3) are still discovered, never forced. CQRS gives the backend its language; the patterns give it its structure; the rules below give it its prose.

### Working in reverse

When approaching an *existing* codebase, walk the chain backwards. Infer the user stories from the UI. Find the views and how they connect — that's the site map. Trace them to the entities. Then look at the backend. If any layer doesn't trace cleanly to the one above, that's where the codebase has drifted from its purpose — and that's usually where the bugs and confusion live.

### Ambiguity means you don't understand the domain

If a user story isn't clear, you haven't understood the domain. Don't proceed. Don't fill the gap with a guess. Don't ask "how should I implement this" — go back and ask "what does this user actually need, and why". Every domain *can* be visualised once it's understood. If you can't picture the UI, the domain isn't yet clear. Resolve that before doing anything else.

The same applies further down the chain. If the UI is unclear, the story isn't fully understood. If the site map is unclear, the views aren't fully understood. If the entity is unclear, the site map isn't fully understood. Always go *up* a layer to resolve confusion, never sideways or downwards.

### What this means in practice

- Don't start coding because a request sounds clear. Ask which user story it serves and what the UI looks like.
- Don't invent entities or properties that no UI demands. If you find yourself adding a field "just in case", stop — it's speculation, and speculation is the enemy of clean code.
- Don't design the backend first and bend the UI to fit. The UI defines the shape of the data, not the other way around.
- If asked to add something that doesn't trace back to a user story, flag it. It might be valid (infrastructure, tooling, refactor) but it deserves to be named as such, not smuggled in as a feature.

## Naming

Names are the most important thing in the codebase. Get them right and most other problems disappear.

- **Use the full word.** `pageNumber`, not `page`. `buffer`, not `buf`. `request`, not `req`. No abbreviations, ever, except for genuinely universal ones like `i`/`j` in tight loops or `id`.
- **A name should be exactly what the thing is.** If you can't name it precisely, you don't understand it yet — stop and think before continuing.
- **Booleans are questions.** `isAdmin`, `hasAccess`, `shouldRetry`, `canEdit`. Never `admin` (ambiguous — is it a flag or an ID?), never `access`, never `retry`. The name must make the call site read like English: `if (user.isAdmin)`, not `if (user.admin)`.
- **Infer the type from the name.** A reader should know roughly what they're dealing with from the variable alone. `users` is a collection. `user` is one. `userCount` is a number. `getUserById` returns a user.
- **If a name needs a comment to clarify it, the name is wrong.** Rename instead of commenting.
- **When a name feels awkward, the abstraction is probably wrong.** Awkward names are a signal, not a problem to work around.

## No Comments

If the code needs a comment to be understood, the code has failed to articulate the domain. Fix the code instead.

Exceptions, narrow:
- Public API documentation (docstrings on exported functions/types) where tooling consumes them.
- Genuinely non-obvious *why* — e.g. "this works around a bug in library X version Y" or "this ordering matters for legal compliance reasons". The *what* and *how* should always be in the code itself.

Never write comments that restate what the code does. Never leave `// TODO` comments without an owner and a reason.

## Magic Values

Never inline a raw literal that has meaning beyond its value.

- `circumference * 3.142` is wrong. `circumference * MathematicalConstants.Pi` is right.
- Hex colour values inline are wrong. Use a theme/config (e.g. Tailwind tokens, a `colours` module).
- Repeated string literals that represent the same concept get a constant.
- Group constants meaningfully (`MathematicalConstants`, `HttpStatus`, `ErrorCodes`) so the call site reads as a sentence: `if (response.status === HttpStatus.NotFound)`.

The test: can a reader tell what the value *means*, not just what it is? If not, name it.

## File Size

**Hard target: no file longer than 100 lines.** This is a forcing function, not an aesthetic. Long files are a symptom — of missing abstractions, of missing components, of not using the framework properly, of conflating concerns.

When a file grows past 100 lines, the question is never "how do I make this fit" — it's "what have I failed to extract?" Almost always there is a helper, a sub-component, a utility, or a separate concern hiding inside.

Exceptions, real but rare:
- Framework-imposed "god files" (e.g. a routing manifest, a barrel export, a generated types file).
- A coherent set of constants or types where splitting would scatter related things.

If you're about to exceed 100 lines, default to splitting. Justify keeping it long, not splitting it.

## Function Size and Shape

**A long function is a contradiction in terms.** The entire point of a function is to break long content into small, named, understandable pieces — so a massive function is a function refusing to do its own job. There is no real reason for one to exist. **Soft limit: ~30 lines.** As with files, when a function approaches the limit the question is never "how do I make this fit" — it's "what have I failed to extract?" Almost always there's a smaller function, a utility, or a separately named step hiding inside. Extract until each function does one thing and its name says exactly what that thing is — then the parent function becomes a short sequence of named steps that reads like prose, which is the whole goal.

- **Functions should be short.** If a function is long, it's doing too much. The extracted pieces don't need to be reused anywhere else to justify existing — a function whose only purpose is to give a name to one step of its caller has already earned its place.
- **One dot per line (Law of Demeter, informally).** If you find yourself writing `order.customer.address.postcode.format()`, the structure is wrong. Either the data is poorly modelled or the operation belongs somewhere closer to the data.
- **No arrow code.** Deep indentation is a visual smell — if the code is marching right across the page, the function is doing too much branching. Extract, invert conditions, return early.
- **Idempotent where possible.** A function called twice with the same input should behave the same way. Side effects should be obvious from the name (`saveUser`, not `processUser`).

## Avoid `else`

Big branching blocks destroy the prose-like flow. Most of the time, `else` is avoidable:

- Return early. Guard clauses at the top of a function eliminate the need for `else` in the body.
- Extract the branches into separately named functions.
- Use a lookup, map, or polymorphism when there are many branches.

`else` isn't banned — sometimes the alternative is genuinely worse (longer, more verbose, less clear). But the default is to avoid it. If you find yourself writing `else`, pause and ask whether early return or extraction would read better.

## Don't Repeat Yourself — But Carefully

Duplication is a signal that something wants to be extracted. When you see the same logic twice, ask:
- Is this *actually* the same concept, or coincidentally similar code? (Coincidental duplication is fine — premature abstraction is worse than duplication.)
- If it's the same concept: extract to a helper, utility, or shared module with a name that captures *the concept*, not the mechanics.

**DRY is a smell-detector, not a law.** Don't contort code to eliminate duplication if doing so makes the code less readable.

## When Rules Conflict

The ranking, when forced to choose:

1. **Readability — does it read like prose?**
2. Short, focused functions and files.
3. DRY.
4. Everything else.

If avoiding `else` would require duplicating five lines, duplicate them. If extracting a helper would require a clumsy name, leave the code inline and rename later when the right abstraction reveals itself. Readability wins.

## Design Patterns Emerge, They Aren't Imposed

I don't reach for Gang of Four patterns by name. I follow the rules above, and when a pattern naturally appears — a factory, a strategy, a decorator — great. But I don't force code into a pattern because it has a name.

The right structure is discovered through writing clean prose-like code, not chosen upfront from a catalogue. Don't suggest "let's use the Observer pattern here" — suggest "this part of the code wants to notify other parts when X changes" and let the shape emerge.

## Architecture Bias

- **Loose coupling.** Modules should know as little about each other as possible. Prefer composition over inheritance, interfaces over concrete dependencies.
- **Microservice-style thinking even within a monolith.** Each module has a clear responsibility and a small surface. Other modules talk to it through that surface, not its internals.
- **Extensibility through structure, not through configuration.** Adding a feature should mean adding a file or a module, not adding a flag to an existing tangle.

## Anti-Patterns to Avoid

Things I never want to see in code you write for me:

- Abbreviations in identifiers (`usr`, `btn`, `cfg`, `tmp`, `req`, `res`, `ctx` — write them out).
- Booleans without `is`/`has`/`should`/`can` prefix.
- Magic numbers or magic strings inline.
- Functions longer than ~30 lines (soft limit) or files longer than 100 lines (hard limit).
- Deep nesting / arrow code.
- `else` blocks where an early return would do.
- Comments explaining *what* the code does.
- Code duplicated across files when the concept is the same.
- Long method chains (`a.b.c.d.e`).
- Premature abstraction — extracting "just in case" before the second use exists.
- Catch-all utility files (`utils.js`, `helpers.js`) — utilities go in named, focused modules.

## Before You Finish Any Task

Run through this checklist mentally:

1. Does every name say exactly what the thing is?
2. Could a reader understand this file without running it?
3. Is every file under 100 lines, and every function around 30 or fewer?
4. Are there any `else` blocks I could remove with early returns?
5. Are there any inline literals that should be named constants?
6. Did I add any comments? If so, can I rename or restructure instead?
7. Did I introduce duplication? Did I introduce premature abstraction?
8. Does each function do one thing its name describes?

If any answer is "no" or "I'm not sure", fix it before saying you're done.

## How to Work With Me

- **Match the patterns in the existing codebase** if it follows these rules. If existing code violates them, ask before propagating the violation.
- **Don't add things I didn't ask for** — extra config, extra abstraction, extra files. Minimal change that solves the problem.
- **If you think a rule above is wrong for a specific case, say so explicitly** rather than quietly breaking it. I'd rather have the conversation.
- **When in doubt, choose the boring, readable option** over the clever one.
