from packaging.specifiers import SpecifierSet
from packaging.version import Version

if __name__ == "__main__":
    # More info: https://packaging.pypa.io/en/latest/specifiers.html

    # Requests 2.26.0 (current version)
    # FastAPI: "requests >=2.24.0,<3.0.0"

    requests_versions = (
        "2.23.0",
        "2.23.1",
        "2.24.0",
        "2.24.1",
        "2.25.0",
        "2.25.1",
        "2.26.0",
        "2.26.1",
        "2.27.0",
        "2.27.1",
        "2.32.0",
        "2.32.1",
        "3.0.0",
    )

    cleo_versions = (
        "0.7.0",
        "0.7.1",
        "0.8.0",
        "0.8.1",
        "0.9.0",
        "0.9.1",
        "1.0.0a1",
        "1.0.0a2",
        "1.0.0",
        "1.0.1",
        "1.1.0",
        "2.0.0",
    )

    # Requests
    spec_fastapi = SpecifierSet(">=2.24.0") & SpecifierSet("<3.0.0")
    spec_half_fastapi = SpecifierSet(">=2.24.0")
    spec_tilde_fastapi = SpecifierSet("~=2.24")

    # Less conservative
    spec_nome = SpecifierSet(">=2.26.0") & SpecifierSet("<3.0.0")
    # More conservative
    spec_tilde_nome = SpecifierSet("~=2.26.0")

    # Cleo
    spec_cleo = SpecifierSet(">=0.8.1") & SpecifierSet("<1.0.0")
    spec_half_cleo = SpecifierSet(">=0.8.1")
    spec_tilde_cleo = SpecifierSet("~=0.8.1")

    # Results
    # Requests
    print(spec_fastapi)
    for version in requests_versions:
        print(f"{version:<6}: {Version(version) in spec_fastapi}")

    print(f"\n{spec_half_fastapi}")
    for version in requests_versions:
        print(f"{version:<6}: {Version(version) in spec_half_fastapi}")

    print(f"\n{spec_tilde_fastapi}")
    for version in requests_versions:
        print(f"{version:<6}: {Version(version) in spec_tilde_fastapi}")

    print(f"\n{spec_nome}")
    for version in requests_versions:
        print(f"{version:<6}: {Version(version) in spec_nome}")

    print(f"\n{spec_tilde_nome}")
    for version in requests_versions:
        print(f"{version:<6}: {Version(version) in spec_tilde_nome}")

    # Cleo
    print(f"\n{spec_cleo}")
    for version in cleo_versions:
        print(f"{version:<6}: {Version(version) in spec_cleo}")

    print(f"\n{spec_half_cleo}")
    for version in cleo_versions:
        print(f"{version:<6}: {Version(version) in spec_half_cleo}")

    print(f"\n{spec_tilde_cleo}")
    for version in cleo_versions:
        print(f"{version:<6}: {Version(version) in spec_tilde_cleo}")
