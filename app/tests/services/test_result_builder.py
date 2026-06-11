from app.models.sequence import SequenceResult
from app.models.variant import Variant
from app.services.result_builder import build_result, fasta_to_raw, render_formatted


def test_fasta_to_raw_strips_header_and_newlines():
    fasta = ">TP53_ALT\nACGT\nACGT"
    assert fasta_to_raw(fasta) == "ACGTACGT"


def test_build_result_uses_alt_sequence_and_variant_metadata():
    variants = [
        Variant(
            gene="TP53",
            cDNA="c.215C>G",
            significance="Pathogenic",
            explanation="腫瘍抑制機能の喪失",
        )
    ]
    sequences = [SequenceResult(fasta_ref=">TP53_REF\nTTTT", fasta_alt=">TP53_ALT\nACGT")]

    result = build_result("Cancer", variants, sequences)

    assert result.disease == "Cancer"
    assert len(result.results) == 1
    item = result.results[0]
    assert item.gene == "TP53"
    assert item.significance == "Pathogenic"
    assert item.explanation == "腫瘍抑制機能の喪失"
    assert item.sequence == "ACGT"  # ALT のみ・生配列


def test_render_formatted_layout():
    variants = [
        Variant(gene="TP53", cDNA="c.1A>T", significance="Pathogenic", explanation="説明A"),
        Variant(gene="BRCA1", cDNA="c.2C>G", significance=None, explanation="説明B"),
    ]
    sequences = [
        SequenceResult(fasta_ref=">r", fasta_alt=">TP53_ALT\nAAAA"),
        SequenceResult(fasta_ref=">r", fasta_alt=">BRCA1_ALT\nCCCC"),
    ]

    text = render_formatted(build_result("Cancer", variants, sequences))

    assert text.splitlines() == [
        "疾患名:Cancer",
        "遺伝子名1:TP53",
        "臨床的意義:Pathogenic / 説明A",
        "塩基配列:AAAA",
        "遺伝子名2:BRCA1",
        "臨床的意義:説明B",
        "塩基配列:CCCC",
    ]
