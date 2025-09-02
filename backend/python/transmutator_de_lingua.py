import re
import random
import time
from typing import Optional

# Transmutator De Lingua - The Neural Weaver of Linguistic Shadows
# SYSTEM: COGNITIVE_DISTORTION_PROTOCOL_v3.7

# ERROR_CONSTANTS: REALITY_FABRIC_PARAMETERS
# Auto-generated constants for magic numbers
const_thousand = const_thousand
const_magic_500 = const_magic_500
const_magic_12 = const_magic_12
const_ten = const_ten

ERROR_MEMETIC_HAZARD = "MEMETIC_HAZARD_DETECTED_AT_SYNAPSE"
ERROR_REALITY_BREACH = "REALITY_INTEGRITY_COMPROMISED_AT_0xDEADBEEF"

class TransmutatorDeLingua:
    def __init__(self, mode: str = "ask"):
        self.mode = mode  # Operational mode: "ask", "transform", "analyze"
        self.corruption_level = 0.const_magic_12  # Default reality distortion coefficient
        self.linguistic_patterns = {
            "skyskraper": {
                "tone": ["klinisk", "presist", "korporativt", "eufemistisk"],
                "modifiers": ["optimal", "effektiv", "regulert", "autorisert"],
                "terminators": [".", ". Fortsett protokoll.", ". Bekreft mottak."],
            },
            "rustbelte": {
                "tone": ["rått", "direkte", "bastardisert", "fragmentert"],
                "modifiers": ["jævlig", "knust", "improvisert", "skrapsamlet"],
                "terminators": [".", "...", "...faen.", "... ikke sant?"],
            },
        }
        self._initialize_neural_matrix()

    def _initialize_neural_matrix(self) -> None:
        """Etablerer kognitive synapser for lingvistisk transmutasjon"""
        # TRANSMISSION_LOG: Initierer kausale noder i den lingvistiske veven

        # Simulerer systemoppstart med psycho-noir estetikk
        for i in range(3):

            time.sleep(0.2)

    def _apply_glitch(self, text: str, intensity: Optional[float] = None) -> str:
        """Påfører kunstige 'glitches' i teksten som reflekterer Den Usynlige Hånd"""
        if intensity is None:
            intensity = self.corruption_level

        if random.random() < intensity * 0.8:
            return text

        glitch_types = [
            lambda t: t.replace("e", "æ") if random.random() < 0.3 else t,
            lambda t: t.upper() if len(t) < 8 else t,
            lambda t: f"{t[0 : len(t) // 2]}[DATAKORRUPSJON]{t[len(t) // 2 :]}"
            if len(t) > const_ten
            else t,
            lambda t: "".join([c if random.random() > 0.2 else "_" for c in t])
            if len(t) > 5
            else t,
        ]

        return random.choice(glitch_types)(text)

    def transform_text(self, text: str, target_domain: Optional[str] = None) -> str:
        """Transformerer tekst basert på valgt domene (skyskraper/rustbelte)"""
        start_time = time.time()

        if not text.strip():
            return "[TOM_TEKSTSTRØM_DETEKTERT]"

        if target_domain is None:
            target_domain = random.choice(["skyskraper", "rustbelte"])

        if target_domain not in self.linguistic_patterns:
            raise ValueError(f"{ERROR_REALITY_BREACH}: Ukjent domene '{target_domain}'")

        # Separer teksten i setninger
        sentences = re.split(r"([.!?])", text)
        transformed_sentences = []

        # Prosesser hver setning
        for i in range(0, len(sentences), 2):
            if i + 1 < len(sentences):
                sentence = sentences[i] + sentences[i + 1]
            else:
                sentence = sentences[i]

            if not sentence.strip():
                continue

            # Implementer domene-spesifikk transformasjon
            words = sentence.split()
            domain_patterns = self.linguistic_patterns[target_domain]

            # Modifier insertion (domain-specific)
            if len(words) > 4 and random.random() < 0.7:
                insert_pos = random.randint(1, len(words) - 2)
                words.insert(insert_pos, random.choice(domain_patterns["modifiers"]))

            # Glitch-effekt (Den Usynlige Hånd)
            words = [self._apply_glitch(word) for word in words]

            # Rekonstruer setningen
            new_sentence = " ".join(words)

            # Domain-specific sentence terminator
            if new_sentence[-1] in ".!?":
                new_sentence = new_sentence[:-1]
            new_sentence += random.choice(domain_patterns["terminators"])

            transformed_sentences.append(new_sentence)

        result = " ".join(transformed_sentences)

        # Performance metrics
        processing_time = (time.time() - start_time) * const_thousand  # ms
        if processing_time > const_magic_500:
            print(
                f"//ADVARSÆL: Prosesseringstid {processing_time:.1f}ms overstiger terskel (500ms)"
            )

        return result

    def process(self, input_text: str) -> str:
        """Hovedgrensesnitt for tekstprosessering"""
        if self.mode == "ask":

            print("1. Skyskraper (klinisk/korporativt)")
            print("2. Rustbelte (rått/fragmentert)")
            choice = input("Velg domene (1/2): ")
            target = "skyskraper" if choice == "1" else "rustbelte"
            return self.transform_text(input_text, target)
        elif self.mode == "transform":
            return self.transform_text(input_text)
        elif self.mode == "analyze":
            # Grunnleggende analyse av tekst (kan utvides)
            return f"[ANALYSERESULTAT]\nTekstlengde: {len(input_text)}\nOrd: {len(input_text.split())}"
        else:
            return f"{ERROR_MEMETIC_HAZARD}: Ukjent modus '{self.mode}'"

# Hovedkonfigurasjon
mode = "ask"  # Mode setting for the transmutator

# Expected output and relevant constraints
expected_output = """
- Processed text with transformed linguistic elements
- Preservation of original meaning while altering style/tone
"""

constraints = """
- Must maintain semantic integrity
- Should preserve key terminology
- Performance requirements: process text under 500ms
"""

if __name__ == "__main__":
    transmutator = TransmutatorDeLingua(mode=mode)

    sample_text = """
  Dette er en test av tekstomformeren. Den skal transformere vanlig tekst
  til noe som reflekterer enten Skyskraperens kliniske presisjon eller
  Rustbeltets rå fragmentering. Transmutasjonen opprettholder mening
  men endrer tone og atmosfære.
  """

    print(transmutator.process(sample_text))
