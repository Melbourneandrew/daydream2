import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Sparkles, Link, Check } from "lucide-react";
import ConceptCard from "@/components/ConceptCard";
import type { ConceptResponse } from "@/types/concept";
import { createApiUrl } from "@/lib/api";

interface Dream {
  id: string;
  created_at: string;
}

interface DreamGetResponse {
  dream: Dream;
  concepts: ConceptResponse[];
}

interface DreamContinueResponse {
  success: boolean;
}

export default function DreamView() {
  const { dreamId } = useParams<{ dreamId: string }>();
  const [isLoading, setIsLoading] = useState(true);
  const [isContinuing, setIsContinuing] = useState(false);
  const [dream, setDream] = useState<Dream | null>(null);
  const [concepts, setConcepts] = useState<ConceptResponse[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  // Load dream data when component mounts or dreamId changes
  useEffect(() => {
    if (dreamId) {
      loadDream();
    }
  }, [dreamId]);

  const loadDream = async () => {
    if (!dreamId) {
      setError("No dream ID provided");
      setIsLoading(false);
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(createApiUrl(`v1/dream/${dreamId}`));
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error("Dream not found");
        }
        throw new Error(`Failed to load dream: ${response.statusText}`);
      }

      const data: DreamGetResponse = await response.json();
      setDream(data.dream);
      setConcepts(data.concepts);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load dream");
    } finally {
      setIsLoading(false);
    }
  };

  const continueDream = async () => {
    if (!dreamId) {
      setError("No dream ID available");
      return;
    }

    setIsContinuing(true);
    setError(null);

    try {
      const response = await fetch(
        createApiUrl(`v1/dream/${dreamId}/continue`),
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error(`Failed to continue dream: ${response.statusText}`);
      }

      const data: DreamContinueResponse = await response.json();
      if (data.success) {
        // Reload the page to show the new concept
        await loadDream();
      } else {
        throw new Error("Dream continuation was not successful");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to continue dream");
    } finally {
      setIsContinuing(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  const copyLink = async () => {
    try {
      await navigator.clipboard.writeText(window.location.href);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("Failed to copy link:", err);
    }
  };

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          <Card>
            <CardContent className="p-8 text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
              <p>Loading your dream...</p>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          <Card className="border-destructive">
            <CardContent className="p-8 text-center">
              <p className="text-destructive mb-4">{error}</p>
              <Button variant="outline" onClick={loadDream}>
                Try Again
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  if (!dream) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          <Card>
            <CardContent className="p-8 text-center">
              <p>Dream not found</p>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-6xl mx-auto space-y-6">
        <div className="text-center">
          <h1 className="text-3xl font-bold mb-2">Dream Journey</h1>
          <p className="text-muted-foreground mb-3 flex items-center justify-center gap-1">
            Started on {formatDate(dream.created_at)} • {concepts.length}{" "}
            concepts •{" "}
            <button
              onClick={copyLink}
              className="ml-1 p-0 bg-transparent border-none cursor-pointer hover:opacity-70 transition-opacity"
              title={copied ? "Copied!" : "Copy link"}
            >
              {copied ? (
                <Check className="h-3 w-3 text-green-600" />
              ) : (
                <Link className="h-3 w-3 text-muted-foreground" />
              )}
            </button>
          </p>
          <p className="text-sm text-muted-foreground max-w-2xl mx-auto">
            Dreams consist of a sequence of concepts. New concepts are generated
            by sampling two previous concepts at random and asking an LLM to
            combine them.
          </p>
        </div>

        {concepts.length < 2 && (
          <Card className="border-yellow-200 bg-yellow-50">
            <CardContent className="p-4">
              <p className="text-yellow-800 text-sm">
                This dream needs at least 2 concepts to continue. Please wait
                for the initial concepts to be generated.
              </p>
            </CardContent>
          </Card>
        )}

        {concepts.length >= 2 && (
          <div className="flex justify-center">
            <Button
              onClick={continueDream}
              disabled={isContinuing}
              size="lg"
              className="px-8 cursor-pointer border-black border-1 font-bold"
            >
              {isContinuing ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Continuing Dream...
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4 mr-2" />
                  Keep Dreaming
                </>
              )}
            </Button>
          </div>
        )}

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {concepts.map((concept) => (
            <ConceptCard key={concept.id} concept={concept} />
          ))}
        </div>
      </div>
    </div>
  );
}
