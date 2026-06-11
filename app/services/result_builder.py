from app.models.sequence import SequenceResult
from app.models.variant import Variant
from app.schemas.result import GeneResult, PipelineResult


def fasta_to_raw(fasta: str) -> str:
    """FASTA テキスト（ヘッダ行 + 改行）から生の塩基配列のみを取り出す。"""
    lines = fasta.splitlines()
    return "".join(line for line in lines if not line.startswith(">"))


def build_result(
    disease: str, variants: list[Variant], sequences: list[SequenceResult]
) -> PipelineResult:
    """variants と sequences（順序対応）から最終出力モデルを組み立てる。

    塩基配列は ALT（変異後）のみを生の塩基列として格納する。
    """
    results = [
        GeneResult(
            gene=variant.gene,
            significance=variant.significance,
            explanation=variant.explanation,
            sequence=fasta_to_raw(seq.fasta_alt),
        )
        for variant, seq in zip(variants, sequences, strict=True)
    ]
    return PipelineResult(disease=disease, results=results)


def render_formatted(result: PipelineResult) -> str:
    """ユーザー指定のレイアウトに整形したテキストを返す。

    疾患名:XXX
    遺伝子名1:YYY
    臨床的意義:ZZZ
    塩基配列:AACCCCTTG...
    """
    lines = [f"疾患名:{result.disease}"]
    for i, r in enumerate(result.results, start=1):
        significance = " / ".join(
            part for part in (r.significance, r.explanation) if part
        )
        lines.append(f"遺伝子名{i}:{r.gene}")
        lines.append(f"臨床的意義:{significance}")
        lines.append(f"塩基配列:{r.sequence}")
    return "\n".join(lines)
