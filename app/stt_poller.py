import os

def poll_stt_outbox_into_session_state(session_state, outbox_path="stt_outbox.txt"):
    if not os.path.exists(outbox_path):
        return
    with open(outbox_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    if not lines:
        return
    for ln in lines:
        try:
            ts, text = ln.strip().split("||", 1)
        except Exception:
            continue
        prev = session_state.get("transcript", "")
        session_state["transcript"] = (prev + " " + text).strip() if prev else text
        session_state.setdefault("chat_history", []).append({"role": "user", "content": text})
    open(outbox_path, "w", encoding="utf-8").close()
