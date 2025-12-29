import textwrap

import snakemd


def readme_feature(
    doc: snakemd.Document,
    main_header: str,
) -> snakemd.Document:

    # Some Specific information

    doc.add_heading(
        text=main_header,
        level=1,
    )

    # Logo

    doc.add_paragraph(
        snakemd.Inline(
            text=textwrap.dedent(
                """\
                Logo Syncthing\
                """
            ),
            image="https://syncthing.net/img/logo-horizontal.svg",
            link="https://syncthing.net/",
        ).__str__()
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """\
            Syncthing is a continuous file synchronization program. 
            It synchronizes files between two or more computers in real 
            time, safely protected from prying eyes. Your data is your 
            data alone and you deserve to choose where it is stored, 
            whether it is shared with some third party, and how it’s 
            transmitted over the internet.\
            """
        )
    )

    doc.add_heading(
        text="Official Documentation",
        level=2,
    )

    doc.add_unordered_list(
        [
            "[Website](https://syncthing.net/)",
            "[Docs](https://docs.syncthing.net/)",
            "[GitHub](https://github.com/syncthing/syncthing)",
        ]
    )

    doc.add_horizontal_rule()

    return doc


if __name__ == "__main__":
    pass
