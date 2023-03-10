import warnings

from courier.elements import AssignPageService, CourierIssue, IssueStatistics


def test_issue_has_no_assigned_pages_as_default():
    issue = CourierIssue('012656')
    assert IssueStatistics(issue).assigned_pages == 0


# FIXME: Check this
def test_AssignArticlesToPages_assignes_expected_pages_to_issue():
    issue = CourierIssue('012656')
    AssignPageService().assign(issue)
    assert issue.get_assigned_pages() == set(
        [7, 8] +                        # 13356
        [11, 12, 13, 14, 15, 32] +      # 14257
        [16, 17, 18, 19, 20, 21] +      # 15043
        [22, 23, 24, 25, 26, 27, 28] +  # 15498
        [29, 30, 31]                    # 16256
    )  # fmt: skip
    assert IssueStatistics(issue).assigned_pages == 24
    assert IssueStatistics(issue).consolidated_pages == 0


def test_AssignArticlesToPages_if_already_assigned_raises_expected_warning():
    courier_id = '012656'
    msg = f'Pages already assigned to {courier_id}'
    issue = CourierIssue(courier_id)

    with warnings.catch_warnings(record=True) as record:
        warnings.simplefilter('always')

        AssignPageService().assign(issue)
        assert len(record) == 0

        AssignPageService().assign(issue)
        assert len(record) == 1
        assert str(record[0].message) == msg
