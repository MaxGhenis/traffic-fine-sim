"""Tests for evidence module - written first following TDD."""

import pytest

from traffic_fines.evidence import SOURCES, EffectSize, Source, get_source, validate_sources


class TestSourceDataclass:
    def test_source_creation(self):
        s = Source(
            id="test1",
            citation="Author (2024)",
            url="https://example.com",
            study_type="theoretical",
            key_finding="Something important",
        )
        assert s.id == "test1"
        assert s.doi is None
        assert s.effect_size is None

    def test_effect_size_creation(self):
        es = EffectSize(
            metric="elasticity",
            point_estimate=0.25,
            ci_lower=0.15,
            ci_upper=0.35,
        )
        assert es.metric == "elasticity"
        assert es.ci_level == 0.95


class TestSourceCount:
    def test_source_count(self):
        """At least 36 sources required."""
        assert len(SOURCES) >= 36


class TestAllSourcesHaveValidUrls:
    def test_all_sources_have_valid_urls(self):
        for s in SOURCES:
            assert s.url.startswith("http"), f"Source {s.id} has invalid URL: {s.url}"


class TestAllSourcesHaveDOIOrDatabase:
    def test_all_sources_have_doi_or_database(self):
        for s in SOURCES:
            assert s.doi or s.database, (
                f"Source {s.id} has neither DOI nor database"
            )


class TestMetaAnalysesHaveEffectSizes:
    def test_meta_analyses_have_effect_sizes(self):
        meta = [s for s in SOURCES if s.study_type == "meta_analysis"]
        assert len(meta) > 0, "Should have at least one meta-analysis"
        for s in meta:
            assert s.effect_size is not None, (
                f"Meta-analysis {s.id} missing effect_size"
            )


class TestGetSource:
    def test_get_source_returns_correct_source(self):
        s = get_source("becker1968")
        assert s is not None
        assert s.id == "becker1968"
        assert "Becker" in s.citation

    def test_get_source_returns_none_for_unknown(self):
        assert get_source("nonexistent_source_xyz") is None


class TestValidateSources:
    def test_validate_sources_returns_no_errors(self):
        errors = validate_sources()
        assert errors == [], f"Validation errors: {errors}"


class TestKeySourcesPresent:
    @pytest.mark.parametrize(
        "source_id",
        ["mirrlees1971", "nilsson2004", "kaila2024", "becker1968", "epa_vsl2024", "policyengine_us2024"],
    )
    def test_key_sources_present(self, source_id):
        s = get_source(source_id)
        assert s is not None, f"Key source {source_id} not found"


class TestEffectSizeValuesReasonable:
    def test_chetty_elasticity_between_0_and_1(self):
        s = get_source("chetty2012")
        assert s is not None
        assert s.effect_size is not None
        assert 0 < s.effect_size.point_estimate < 1

    def test_nilsson_power_exponent_reasonable(self):
        s = get_source("nilsson2004")
        assert s is not None
        assert s.effect_size is not None
        # Power model exponent for fatalities ~4
        assert 2 < s.effect_size.point_estimate < 6

    def test_confidence_intervals_ordered(self):
        for s in SOURCES:
            if s.effect_size and s.effect_size.ci_lower is not None:
                assert s.effect_size.ci_lower <= s.effect_size.point_estimate, (
                    f"{s.id}: ci_lower > point_estimate"
                )
                assert s.effect_size.point_estimate <= s.effect_size.ci_upper, (
                    f"{s.id}: point_estimate > ci_upper"
                )


class TestStudyTypes:
    def test_valid_study_types(self):
        valid = {
            "meta_analysis",
            "rct",
            "quasi_experimental",
            "theoretical",
            "administrative",
            "survey",
            "review",
        }
        for s in SOURCES:
            assert s.study_type in valid, (
                f"Source {s.id} has invalid study_type: {s.study_type}"
            )
