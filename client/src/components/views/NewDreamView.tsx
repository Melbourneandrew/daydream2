import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Dices, Sparkles } from "lucide-react";

interface GeneratedConcept {
  content: string;
}

interface DreamCreateResponse {
  concepts: GeneratedConcept[];
}

interface DreamStartRequest {
  concept_1: string;
  concept_2: string;
}

interface DreamStartResponse {
  success: boolean;
  dream_id: string;
}

export default function NewDreamView() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [isStarting, setIsStarting] = useState(false);
  const [concept1, setConcept1] = useState("");
  const [concept2, setConcept2] = useState("");
  const [error, setError] = useState<string | null>(null);

  // Generate initial concepts when component mounts
  useEffect(() => {
    generateInitialConcepts();
  }, []);

  const generateInitialConcepts = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch("http://localhost:8000/v1/dream/new");
      if (!response.ok) {
        throw new Error(`Failed to generate concepts: ${response.statusText}`);
      }

      const data: DreamCreateResponse = await response.json();
      setConcept1(data.concepts[0]?.content || "");
      setConcept2(data.concepts[1]?.content || "");
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to generate concepts"
      );
    } finally {
      setIsLoading(false);
    }
  };

  const startDreaming = async () => {
    if (!concept1.trim() || !concept2.trim()) {
      setError("Both concepts must be filled in");
      return;
    }

    setIsStarting(true);
    setError(null);

    try {
      const requestBody: DreamStartRequest = {
        concept_1: concept1.trim(),
        concept_2: concept2.trim(),
      };

      const response = await fetch("http://localhost:8000/v1/dream/start", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`Failed to start dream: ${response.statusText}`);
      }

      const data: DreamStartResponse = await response.json();
      if (data.success && data.dream_id) {
        navigate(`/dream/${data.dream_id}`);
      } else {
        throw new Error("Dream start was not successful");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to start dream");
    } finally {
      setIsStarting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          <Card>
            <CardContent className="p-8 text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
              <p>Generating some initial concepts for the dream...</p>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-2xl mx-auto space-y-6">
        <div className="text-center">
          <h1 className="text-3xl font-bold mb-2">Start a New Dream</h1>
          <p className="text-muted-foreground">
            Dreams begin with two concepts that are combined by AI to create a
            new concept. From there, each new concept is created by combining
            two randomly selected concepts from your dream's history.
          </p>
        </div>

        {error ? (
          <Card className="border-destructive">
            <CardContent className="p-4">
              <p className="text-destructive text-sm">{error}</p>
              <Button
                variant="outline"
                size="sm"
                onClick={generateInitialConcepts}
                className="mt-2"
              >
                Try Again
              </Button>
            </CardContent>
          </Card>
        ) : concept1 && concept2 ? (
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Concept 1</CardTitle>
                <CardDescription>Edit this concept as you like</CardDescription>
              </CardHeader>
              <CardContent>
                <textarea
                  value={concept1}
                  onChange={(e) => setConcept1(e.target.value)}
                  className="w-full min-h-[100px] p-3 border rounded-md resize-none"
                  placeholder="Enter your first concept..."
                />
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Concept 2</CardTitle>
                <CardDescription>Edit this concept as you like</CardDescription>
              </CardHeader>
              <CardContent>
                <textarea
                  value={concept2}
                  onChange={(e) => setConcept2(e.target.value)}
                  className="w-full min-h-[100px] p-3 border rounded-md resize-none"
                  placeholder="Enter your second concept..."
                />
              </CardContent>
            </Card>

            <div className="flex justify-center gap-4">
              <Button
                variant="outline"
                onClick={() => window.location.reload()}
                size="lg"
                className="px-8"
              >
                <Dices className="w-4 h-4 mr-2" />
                Re-roll Concepts
              </Button>
              <Button
                onClick={startDreaming}
                disabled={isStarting || !concept1.trim() || !concept2.trim()}
                size="lg"
                className="px-8"
              >
                {isStarting ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Starting Dream...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4 mr-2" />
                    Start Dreaming
                  </>
                )}
              </Button>
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}
