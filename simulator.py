"""A small, seeded civilization history simulator."""

import argparse
import random
from dataclasses import dataclass, field


CITY_NAMES = (
    "Aster", "Briar", "Cairn", "Dara", "Eldin", "Fallow",
    "Glenhaven", "Harrow", "Iria", "Jora", "Kestrel", "Linden",
)
GOVERNMENTS = ("council", "monarchy", "republic", "confederation")
RELIGIONS = ("Sun Path", "River Faith", "Star Tradition", "Earth Covenant")
TECHNOLOGIES = (
    "irrigation", "masonry", "writing", "ironworking", "road building",
    "navigation", "medicine", "printing", "mechanics", "astronomy",
    "banking", "engineering", "agronomy", "public sanitation",
)


@dataclass
class City:
    name: str
    founded: int
    population: int
    religion: str
    wealth: int


@dataclass
class Report:
    start_year: int
    end_year: int
    government: str
    cities: list[City]
    technologies: list[str]
    discoveries: list[str]
    wars: list[str]
    records: list[str]


@dataclass
class Civilization:
    rng: random.Random
    government: str = "council"
    cities: list[City] = field(default_factory=list)
    technologies: list[str] = field(default_factory=list)

    def found_city(self, year: int) -> str:
        name = CITY_NAMES[len(self.cities)]
        city = City(
            name=name,
            founded=year,
            population=self.rng.randint(800, 2400),
            religion=self.rng.choice(RELIGIONS),
            wealth=self.rng.randint(500, 1500),
        )
        self.cities.append(city)
        return f"Year {year}: {name} was founded with {city.population:,} inhabitants."

    def simulate(self) -> list[Report]:
        """Advance 1,000 individual years and snapshot each century."""
        founding = self.found_city(1)
        reports = []
        records: list[str] = []
        wars: list[str] = []
        discoveries: list[str] = []
        records.append(founding)

        for year in range(1, 1001):
            if year > 1 and len(self.cities) < len(CITY_NAMES) and self.rng.random() < 0.012:
                records.append(self.found_city(year))

            for city in self.cities:
                growth = self.rng.uniform(0.002, 0.012)
                city.population += max(1, int(city.population * growth * (1 - city.population / 2_000_000)))
                # Wealth represents accumulated local economic output, in abstract units.
                city.wealth += max(1, int(city.population * self.rng.uniform(0.02, 0.05)))

            if self.rng.random() < 0.006:
                old = self.government
                self.government = self.rng.choice([g for g in GOVERNMENTS if g != old])
                records.append(f"Year {year}: Government changed from {old} to {self.government}.")

            if self.rng.random() < 0.008:
                city = self.rng.choice(self.cities)
                old = city.religion
                city.religion = self.rng.choice([r for r in RELIGIONS if r != old])
                records.append(f"Year {year}: {city.name} shifted from {old} to {city.religion}.")

            if len(self.technologies) < len(TECHNOLOGIES) and self.rng.random() < 0.025:
                technology = TECHNOLOGIES[len(self.technologies)]
                self.technologies.append(technology)
                event = f"Year {year}: {technology} was developed."
                discoveries.append(event)
                records.append(event)

            if len(self.cities) >= 2 and self.rng.random() < 0.015:
                attacker, defender = self.rng.sample(self.cities, 2)
                losses_a = max(1, int(attacker.population * self.rng.uniform(0.01, 0.04)))
                losses_d = max(1, int(defender.population * self.rng.uniform(0.01, 0.04)))
                attacker.population -= losses_a
                defender.population -= losses_d
                defender.wealth = max(0, defender.wealth - int(defender.wealth * 0.05))
                event = (
                    f"Year {year}: {attacker.name} fought {defender.name}; "
                    f"population losses were {losses_a:,} and {losses_d:,}, respectively."
                )
                wars.append(event)
                records.append(event)

            if year % 10 == 0:
                population = sum(city.population for city in self.cities)
                wealth = sum(city.wealth for city in self.cities)
                records.append(
                    f"Year {year}: Census recorded {population:,} people in "
                    f"{len(self.cities)} {'city' if len(self.cities) == 1 else 'cities'}; "
                    f"wealth was {wealth:,} units."
                )

            if year % 100 == 0:
                reports.append(Report(
                    start_year=year - 99,
                    end_year=year,
                    government=self.government,
                    cities=[City(**vars(city)) for city in self.cities],
                    technologies=self.technologies.copy(),
                    discoveries=discoveries,
                    wars=wars,
                    records=records,
                ))
                records, wars, discoveries = [], [], []

        return reports


def simulate(seed: int = 0) -> list[Report]:
    return Civilization(random.Random(seed)).simulate()


def format_report(report: Report) -> str:
    population = sum(city.population for city in report.cities)
    wealth = sum(city.wealth for city in report.cities)
    lines = [
        f"=== Years {report.start_year}-{report.end_year} ===",
        f"Government at century end: {report.government}",
        f"Economy: {population:,} people; {wealth:,} total wealth units.",
        "Cities and religions at century end:",
    ]
    for city in report.cities:
        lines.append(
            f"  {city.name} (founded {city.founded}): {city.population:,} people, "
            f"{city.wealth:,} wealth units, {city.religion}."
        )
    lines.append("Technologies known: " + (", ".join(report.technologies) or "none"))
    lines.append("Discoveries this century:")
    lines.extend(f"  {event}" for event in report.discoveries or ["None."])
    lines.append("Wars this century:")
    lines.extend(f"  {event}" for event in report.wars or ["None."])
    lines.append("Historical records:")
    lines.extend(f"  {event}" for event in report.records)
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulate 1,000 years of civilization.")
    parser.add_argument("--seed", type=int, default=0, help="random seed (default: 0)")
    args = parser.parse_args()
    print("\n\n".join(format_report(report) for report in simulate(args.seed)))


if __name__ == "__main__":
    main()
