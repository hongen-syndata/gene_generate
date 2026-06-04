import os

from app.models.sequence import SequenceResult
from app.models.snp import SNP
from app.utils.llm_client import call_llm


def load_prompt():
    base_dir = os.path.dirname(__file__)  # app/services/
    prompt_path = os.path.join(base_dir, "..", "prompts", "fasta_prompt.txt")
    prompt_path = os.path.abspath(prompt_path)

    with open(prompt_path, encoding="utf-8") as f:
        return f.read()


def render_prompt(template: str, gene: str, pos: int, window: int) -> str:
    return (
        template.replace("{{gene}}", gene)
        .replace("{{pos}}", str(pos))
        .replace("{{window}}", str(window))
    )


# -----------------------------
# Variant handlers
# -----------------------------


def handle_substitution(ref_seq: str, pos: int, ref: str, alt: str):
    # REF と ALT が 1 塩基のときだけ
    if len(ref) == 1 and len(alt) == 1 and ref in "ATCG" and alt in "ATCG":
        idx = pos - 1
        return ref_seq[:idx] + alt + ref_seq[idx + 1 :]
    return None


def handle_deletion(ref_seq: str, pos: int, ref: str, alt: str):
    if alt == "-" and ref != "-":
        idx = pos - 1
        return ref_seq[:idx] + ref_seq[idx + 1 :]
    return None


VARIANT_HANDLERS = [
    handle_substitution,
    handle_deletion,
    # handle_insertion,
    # handle_delins,
    # handle_dup,
]


def apply_variant(ref_seq: str, pos: int, ref: str, alt: str) -> str:
    for handler in VARIANT_HANDLERS:
        result = handler(ref_seq, pos, ref, alt)
        if result is not None:
            return result

    raise ValueError(f"Unsupported variant type: ref={ref}, alt={alt}")


# -----------------------------
# FASTA formatting
# -----------------------------


def to_fasta(header: str, sequence: str, line_width: int = 60) -> str:
    lines = [sequence[i : i + line_width] for i in range(0, len(sequence), line_width)]
    seq_block = "\n".join(lines)
    return f">{header}\n{seq_block}"


# -----------------------------
# Sequence generation (内部モデル対応)
# -----------------------------


def generate_sequence(snp: SNP) -> SequenceResult:
    gene = snp.gene
    pos = snp.pos
    window = 100
    line_width = 60

    # ① プロンプト生成
    template = load_prompt()
    prompt = render_prompt(template, gene, pos, window)

    # ② LLM で REF 配列生成
    llm_output = call_llm(prompt)
    ref_seq = llm_output.strip()

    # ③ REF → ALT 変換
    alt_seq = apply_variant(ref_seq=ref_seq, pos=snp.pos, ref=snp.ref, alt=snp.alt)

    # ④ FASTA 形式に整形
    fasta_ref = to_fasta(header=f"{snp.gene}_REF", sequence=ref_seq, line_width=line_width)
    fasta_alt = to_fasta(header=f"{snp.gene}_ALT", sequence=alt_seq, line_width=line_width)

    return SequenceResult(fasta_ref=fasta_ref, fasta_alt=fasta_alt)
