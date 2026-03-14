# 🌉 JAO: Manual Bridge Protocol (Human-as-Orchestrator)

While the **Autonomous Orchestrator Engine** is being finalized, you can operate the **Cybernetic Firm** manually. All agents have been synchronized to follow this protocol.

### Where are the files?
All agents are instructed to save their work to a standardized directory:
📂 `c:\Users\vamsh\Desktop\jules agents personas\jewels_agents\JAO\sessions\[SESSION_ID]\inbox\`

---

## 🏗️ The 5-Step Workflow (A-E)

To maintain 100% consistency with the future autonomous system, you must act as the "Context Bridge" between agents.

### Step 1: Design Phase (@ada)
1. **Activate**: Spawn a session with `@ada`.
2. **Task**: Give her your high-level requirement.
3. **Outcome**: Ada will write `JAO-[ID]-A_BLUEPRINT.md` to your `JAO/sessions/` folder.
4. **Action**: Copy the *entire contents* of that Blueprint file.

### Step 2: Prompt Engineering Phase (@priya)
1. **Activate**: Spawn a session with `@priya`.
2. **Task**: Paste the Blueprint content and say: "Synthesize the developer prompt for this."
3. **Outcome**: Priya will write `JAO-[ID]-B_PROMPT.md`.
4. **Action**: Copy the *Developer Prompt* section from that file.

### Step 3: Implementation Phase (@pydan / @rita)
1. **Activate**: Spawn the relevant developer agent (`@pydan` for Backend, `@rita` for Frontend).
2. **Task**: Paste the Developer Prompt from Priya.
3. **Outcome**: The agent will implement the code and write `JAO-[ID]-C_LOG.md`.
4. **Action**: Copy the verification/test steps from their log.

### Step 4: Quality Assurance Phase (@tina)
1. **Activate**: Spawn `@tina`.
2. **Task**: Paste the implementation log and the verification steps.
3. **Outcome**: Tina will run tests and write `JAO-[ID]-D_REPORT.md`.
4. **Action**: Copy the final test status (PASS/FAIL).

### Step 5: Final Review Phase (@vera)
1. **Activate**: Spawn `@vera`.
2. **Task**: Paste the Blueprint (A) and the Test Report (D) and say: "Verify and provide final decision."
3. **Outcome**: Vera will write `JAO-[ID]-E_DECISION.md`.
4. **Final Action**: If "GREEN LIGHT," you can merge the changes to your `main` branch.

---

## 💡 Pro-Tips for the Human Orchestrator
- **Persistence**: Always ensure the `.md` files are saved in the project folder. This is the "Long Term Memory" of your firm.
- **Strictness**: If an agent tries to talk to you instead of writing a file, remind them: "Follow the Baton-Pass protocol and write to the session inbox."
---

## 🚀 How to Start the Project RIGHT NOW (Manual Mode)

If you want to start building the JAO project today using your agents, follow this exact sequence:

### 1. The Startup Command
Go to Jules and paste the persona of **`ada_architect.md`**.
Then give her this one sentence:
> "Bootstrap: Read `JAO/sessions/PHASE1_ENGINE/inbox/JAO-PHASE1-A_TASK.md` and design the implementation blueprint for the Core Engine."

### 2. Follow the Baton
- **Ada (A)** will output a Blueprint to that folder.
- **You** copy that file content and give it to **`priya_promptcraft.md`**.
- **You** copy Priya's output to **`py_dan_backend.md`**.
- and so on...

---
