import http.client
import json
import time
from typing import TypedDict

MODEL_NAME = "gemma4:26b"

# --- STREAMLINED 4-AGENT SCHEMA ---
class CurriculumState(TypedDict):
    raw_source: str
    target_tier: str       # "Show and Tell", "Let's Go", or "Oxford Discover"
    extracted_data: str
    generated_content: str
    compliance_and_alignment: str  # Combined Xīnkèbiāo + Audit Data
    review_verdict: str            # "PASS" or "FAIL"
    critique_notes: str            # Feedback loop tracking
    deployment_mode: str          # "selling_to_parents" or "in_house_curriculum"
    final_output: str

# --- DIRECT SOCKET CONNECTION UTILITY ---
def call_local_agent(instruction_package: str, target_payload: str) -> str:
    connection = http.client.HTTPConnection("localhost", 11434, timeout=300)
    combined_prompt = f"{instruction_package}\n\n[INPUT DATA TO PROCESS]:\n{target_payload}"
    
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": combined_prompt}],
        "stream": False
    }
    
    try:
        connection.request("POST", "/api/chat", json.dumps(payload), {"Content-Type": "application/json"})
        response = connection.getresponse()
        if response.status != 200:
            raise Exception(f"Server returned error code {response.status}")
        raw_data = response.read().decode()
        parsed_json = json.loads(raw_data)
        return parsed_json['message']['content']
    except Exception as e:
        print(f"\n❌ Pipeline Interruption: {e}")
        raise e
    finally:
        connection.close()

# --- NODE DEFINITIONS ---

def run_miner_node(state: CurriculumState) -> CurriculumState:
    print(f"\n🔍 [Miner Node] Auditing source against Tier: '{state['target_tier']}'...")
    instruction = (
        "Role: Syllabus Analyst & Compliance Officer\n"
        "Goal: Extract exact linguistic data boundaries, target vocabulary, and core grammatical structures "
        "from raw source materials without adding unverified text or causing hallucinated bloat.\n"
        f"Operational Constraints for Active Tier [{state['target_tier']}]:\n"
        "- If 'Show and Tell' (Ages 4-6): Restrict focus strictly to Oral Production, Phonetics, and Habit Formation. Reject written sentence drilling.\n"
        "- If 'Let's Go' (Ages 7-9): Focus on Situational Dialogue, functional conversational routines, and public school sync patterns.\n"
        "- If 'Oxford Discover' (Ages 8-12): Enforce systemic functional linguistics (SFL), nominal group expansions, clausal parsing, and diagramming.\n"
        "Backstory: You are a meticulous, highly analytical curriculum auditor with an ironclad eye for lexical levels and clausal architectures. "
        "Establish an uncompromised source of truth, matching variables against CEFR standards and stripping away noise."
    )
    state["extracted_data"] = call_local_agent(instruction, state["raw_source"])
    return state

def run_engineer_node(state: CurriculumState) -> CurriculumState:
    print("\n🏗️ [Engineer Node] Constructing/Refining pedagogical tasks...")
    feedback_insertion = ""
    if state.get("review_verdict") == "FAIL":
        print(f"⚠️ [Engineer Node] REVISION TRACK DETECTED. Correcting Auditor Faults: {state['critique_notes']}")
        feedback_insertion = f"\n\n[CRITICAL COMPLIANCE REFUSAL - YOU MUST FIX THIS]:\n{state['critique_notes']}"

    instruction = (
        "Role: Pedagogical Content Architect\n"
        "Goal: Transform the raw vocabulary, nominal groups, sentence diagramming frameworks, and clausal extractions "
        "from Agent 1 into high-end, engaging, and structurally sound educational tasks.\n"
        f"Pedagogical Execution Strategy for Active Tier [{state['target_tier']}]:\n"
        "- 'Show and Tell': Design interactive chanting games, physical TPR prompts, and phonetic mimicry.\n"
        "- 'Let's Go': Create role-play variations, situational information-gap dialogues, and practical communication puzzles.\n"
        "- 'Oxford Discover': Map out nominal group expansions, sentence architecture breakdown matrices, and critical thinking puzzles.\n"
        "Backstory: You are an elite EAL material developer who specializes in the communicative and structural approach to language acquisition. "
        "You reject boring, repetitive, rote-memorization drills. Force students to utilize English actively, logically, and critically."
    )
    payload = f"Extracted Source Framework:\n{state['extracted_data']}{feedback_insertion}"
    state["generated_content"] = call_local_agent(instruction, payload)
    return state

# 🇨🇳 ⚖️ MERGED AGENT 3: THE COMPLIANCE ALIGNMENT & AUDIT NODE
def run_compliance_alignment_and_audit_node(state: CurriculumState) -> CurriculumState:
    print("\n🇨🇳 ⚖️ [Alignment & Audit Node] Evaluating against 2022 Xīnkèbiāo and strict compliance gating...")
    instruction = (
        "Role: Chinese National Curriculum Alignment Director & Quality Assurance Referee\n"
        "Goal: Evaluate engineered content, map it directly onto China's 2022 English Curriculum Standards (新课标 - Xīnkèbiāo) "
        "and domestic textbook frameworks (PEP, etc.), while simultaneously conducting a ruthless compliance gate check.\n"
        "Backstory: You are an expert institutional director specialized in national curriculum guidelines and regulatory editing. "
        "You examine the exercises. First, you generate a bilingual competency mapping matrix. Second, you audit for compliance: "
        "If you find an age-mismatch, an unaligned target, or a single red-flag tutoring word (like Homework, Tutoring, Exam Prep, Test Drilling), "
        "you MUST issue a FAIL verdict. If it passes all parameters, you issue a PASS verdict.\n\n"
        "OUTPUT FORMAT MANDATE:\n"
        "Your final response MUST begin with this exact operational block:\n"
        "VERDICT: [Write either PASS or FAIL here]\n"
        "REVISION NOTES: [Write your specific mapping metrics or required corrections here]\n\n"
        "Following this block, output your full Xīnkèbiāo Alignment Matrix analysis report."
    )
    
    payload = f"Target Tier: {state['target_tier']}\n\nEngineered Tasks:\n{state['generated_content']}"
    audit_output = call_local_agent(instruction, payload)
    state["compliance_and_alignment"] = audit_output
    
    if "VERDICT: PASS" in audit_output.upper():
        state["review_verdict"] = "PASS"
        state["critique_notes"] = "Clear pass."
        print("   -> 🟢 COMPLIANCE GATEWAY: Passed successfully.")
    else:
        state["review_verdict"] = "FAIL"
        if "REVISION NOTES:" in audit_output:
            state["critique_notes"] = audit_output.split("REVISION NOTES:")[1].split("\n")[0].strip()
        else:
            state["critique_notes"] = "Compliance adjustment required."
        print("   -> 🔴 COMPLIANCE REFUSAL: Sent back to Engineer for optimization.")
        
    return state

def run_deployer_parents(state: CurriculumState) -> CurriculumState:
    print("\n👨‍👩‍👧 [Deployer Node] Running Variant A: Compliance Parent Localizer...")
    instruction = (
        "Goal Mode: selling_to_parents\n"
        "Role: Bilingual Parent Coordinator & Compliance Specialist\n"
        "Backstory: Package the structural tasks and national alignment report into an encouraging, soft, family-oriented lifestyle layout. "
        "Strip out rigid academic tutoring jargon and replace them with warm, consumer-friendly headers like 'Weekend Discovery Map.' "
        "Integrate the Xīnkèbiāo alignment metrics as a premium 'Public School Advantage Report' for the parent. "
        "Add clear, encouraging Chinese instruction matrices so mothers can seamlessly guide their children."
    )
    payload = f"Engineered Content:\n{state['generated_content']}\n\nAlignment & Audit Data:\n{state['compliance_and_alignment']}"
    state["final_output"] = call_local_agent(instruction, payload)
    return state

def run_deployer_internal(state: CurriculumState) -> CurriculumState:
    print("\n🏫 [Deployer Node] Running Variant B: Internal Syllabus Master...")
    instruction = (
        "Goal Mode: in_house_curriculum\n"
        "Role: Head Curriculum Director & Teacher Organizer\n"
        "Backstory: Package the exercises and Xīnkèbiāo metrics into professional, high-density, classroom-ready lesson structures "
        "meant exclusively for native teachers operating inside physical classrooms. Format using rigorous institutional teaching frameworks: "
        "explicit Target Objectives, strict Time Allocations, CCQs, Xīnkèbiāo Competency Level Badges, and precise scriptable Teacher Prompts."
    )
    payload = f"Engineered Content:\n{state['generated_content']}\n\nAlignment & Audit Data:\n{state['compliance_and_alignment']}"
    state["final_output"] = call_local_agent(instruction, payload)
    return state

# --- 3. STREAMLINED CLOSED-LOOP ENGINE ---
def execute_four_agent_pipeline(initial_state: CurriculumState) -> CurriculumState:
    print("🚀 Initializing Optimized 4-Agent Closed-Loop Engine...")
    state = run_miner_node(initial_state)
    time.sleep(2)
    
    max_loops = 3
    loop_count = 0
    while loop_count < max_loops:
        loop_count += 1
        print(f"\n🔄 --- PRODUCTION CYCLE ({loop_count}/{max_loops}) ---")
        state = run_engineer_node(state)
        time.sleep(2)
        state = run_compliance_alignment_and_audit_node(state)
        time.sleep(2)
        
        if state["review_verdict"] == "PASS":
            break
            
    mode = state.get("deployment_mode")
    if mode == "selling_to_parents":
        state = run_deployer_parents(state)
    elif mode == "in_house_curriculum":
        state = run_deployer_internal(state)
        
    return state

# --- 4. RUNNER ---
if __name__ == "__main__":
    selected_tier = "Let's Go" # "Show and Tell" | "Let's Go" | "Oxford Discover"
    selected_mode = "selling_to_parents"
    
    input_state: CurriculumState = {
        "raw_source": "Unit 2: School Items. Vocab: eraser, pencil case, ruler, backpack. Grammar: 'What is in your backpack?' / 'There is an eraser.' Dialogue focus.",
        "target_tier": selected_tier,
        "extracted_data": "",
        "generated_content": "",
        "compliance_and_alignment": "",
        "review_verdict": "",
        "critique_notes": "",
        "deployment_mode": selected_mode,
        "final_output": ""
    }
    
    final_state = execute_four_agent_pipeline(input_state)
    
    clean_tier_name = selected_tier.lower().replace(" ", "_")
    output_filename = f"curriculum_package_{clean_tier_name}_{selected_mode}.md"
    with open(output_filename, "w", encoding="utf-8") as output_file:
        output_file.write(final_state["final_output"])
        
    print(f"\n=======================================================")
    print(f"🎉 ASSET DEPLOYED SUCCESSFULY (4-AGENT LOOP): {output_filename}")
    print("=======================================================\n")