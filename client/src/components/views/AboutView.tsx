export default function AboutView() {
  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6 text-left text-lg">
      <h1
        className="text-3xl font-bold mb-8"
        style={{ color: "var(--solarized-base03)" }}
      >
        About Daydream
      </h1>

      <div className="space-y-6">
        <p
          className="text-lg leading-relaxed mb-6"
          style={{ color: "var(--solarized-base01)" }}
        >
          Daydream is inspired by the Gwern.net essay{" "}
          <a
            href="https://gwern.net/ai-daydreaming"
            target="_blank"
            rel="noopener noreferrer"
            className="font-bold underline"
            style={{ color: "var(--link-color)" }}
          >
            LLM Daydreaming
          </a>
          , where he introduces the concept of an AI system that continuously
          combines concepts to generate novel insights and ideas.
        </p>

        <div
          className="p-6 my-8 rounded-lg"
          style={{
            backgroundColor: "var(--card-background)",
            borderLeft: "4px solid var(--button-background)",
          }}
        >
          <blockquote
            className="italic leading-relaxed mb-4"
            style={{ color: "var(--solarized-base01)" }}
          >
            "To illustrate the issue, I describe such insights, and give an
            example concrete algorithm of a day-dreaming loop (DDL): a
            background process that continuously samples pairs of concepts from
            memory. A generator model explores non-obvious links between them,
            and a critic model filters the results for genuinely valuable ideas.
            These discoveries are fed back into the system's memory, creating a
            compounding feedback loop where new ideas themselves become seeds
            for future combinations."
          </blockquote>
          <cite className="block text-right text-sm font-semibold px-2 py-1 rounded inline-block">
            — Gwern Branwen
          </cite>
        </div>
        <p style={{ color: "var(--solarized-base01)" }}>
          This site implements a rudimentary system in the spirit of Gwern's DDL
          algorithm. A new dream is initiated with two randomly generated
          concepts that an LLM combines to create a third concept. The user can
          then continue the dream by generating a new concept created from two
          randomly selected concepts that were previously generated in the
          dream.
        </p>
        <p style={{ color: "var(--solarized-base01)" }}>
          This was built on a Saturday afternoon in August of 2025 using the{" "}
          <a
            href="https://8090.ai"
            target="_blank"
            rel="noopener noreferrer"
            className="font-bold underline"
            style={{ color: "var(--link-color)" }}
          >
            8090 Software Factory.
          </a>
        </p>
      </div>
    </div>
  );
}
