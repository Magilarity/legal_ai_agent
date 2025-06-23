import os

import prozorro_loader
from app import (
    document_loader,
    embedder,
    export_utils,
    llm_agent,
    sign_extractor,
    text_splitter,
    vector_store,
)


def analyze_tender_by_id(tender_id: str) -> str:
    temp_dir = "documents"
    prozorro_loader.download_documents(tender_id, temp_dir)

    result_texts = []
    signatures = []

    for filename in os.listdir(temp_dir):
        full_path = os.path.join(temp_dir, filename)

        if filename.lower().endswith((".pdf", ".docx")):
            text = document_loader.extract_text_from_file(full_path)
            if not text or not text.strip():
                result_texts.append(f"📄 {filename}\n[WARNING] Порожній документ.")
                continue

            chunks = text_splitter.split_text(text)
            if not chunks:
                result_texts.append(
                    f"📄 {filename}\n[WARNING] Не вдалося розбити текст."
                )
                continue

            embeddings = embedder.embed_chunks(chunks)
            if not embeddings or not embeddings[0]:
                result_texts.append(f"📄 {filename}\n[WARNING] Помилка векторизації.")
                continue

            index = vector_store.create_index(embeddings)
            top_indices = vector_store.search_index(index, embeddings[0])
            # Фільтруємо невірні індекси
            valid = [chunks[i] for i in top_indices if 0 <= i < len(chunks)]
            if not valid:
                result_texts.append(
                    f"📄 {filename}\n[WARNING] Нема релевантних фрагментів."
                )
                continue

            context = "\n---\n".join(valid)
            answer = llm_agent.generate_answer(
                context, f"Правовий зміст документа {filename}:"
            )
            # Якщо generate_answer повернув помилку — показуємо її
            if answer.startswith("[ERROR]"):
                result_texts.append(f"📄 {filename}\n{answer}")
            else:
                result_texts.append(f"📄 {filename}\n{answer}")

        elif filename.lower().endswith(".p7s"):
            info = sign_extractor.extract_signature_info(full_path)
            for signer in info:
                parts = [f"{k}: {v}" for k, v in signer.items()]
                signatures.append(f"🔏 {filename}: " + ", ".join(parts))

    final = "\n\n".join(result_texts)
    # Тепер export_utils не логує в потоці, а викидає виключення, якщо щось не так
    export_utils.save_analysis_to_docx(tender_id, final, signatures)
    export_utils.save_analysis_to_pdf(tender_id, final, signatures)

    return final
