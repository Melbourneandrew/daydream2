import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { ConceptResponse } from "@/types/concept";

interface ConceptCardProps {
  concept: ConceptResponse;
  className?: string;
}

export default function ConceptCard({ concept, className }: ConceptCardProps) {
  const getConceptType = (concept: ConceptResponse) => {
    if (!concept.parent1_id && !concept.parent2_id) {
      return "Initial";
    }
    return "Generated";
  };

  const getConceptVariant = (concept: ConceptResponse) => {
    if (!concept.parent1_id && !concept.parent2_id) {
      return "secondary" as const;
    }
    return "default" as const;
  };

  const handleParentClick = (parentId: string) => {
    // Find the parent concept in the current concepts list and scroll to it
    const parentElement = document.getElementById(`concept-${parentId}`);
    if (parentElement) {
      parentElement.scrollIntoView({ behavior: "smooth", block: "center" });
      // Add a temporary highlight effect using button color
      parentElement.style.boxShadow = "0 0 0 2px var(--button-background)";
      parentElement.style.borderColor = "var(--button-background)";
      setTimeout(() => {
        parentElement.style.boxShadow = "";
        parentElement.style.borderColor = "";
      }, 2000);
    }
  };

  return (
    <Card
      id={`concept-${concept.id}`}
      className={`${className || ""} min-h-[150px]`}
    >
      <CardContent className="p-6">
        {/* Main content - displayed prominently */}
        <div className="mb-4">
          <p className="text-base leading-relaxed min-h-[52px]">
            {concept.content}
          </p>
        </div>

        {/* Parent information at the bottom */}
        <div className="flex items-center justify-between pt-3 border-t">
          <Badge variant={getConceptVariant(concept)}>
            {getConceptType(concept)}
          </Badge>
          <div className="flex items-center gap-2">
            {concept.parent1_id && concept.parent2_id ? (
              <>
                <span className="text-xs text-muted-foreground">Parents:</span>
                <Badge
                  variant="secondary"
                  className="cursor-pointer text-xs transition-colors"
                  onClick={() => handleParentClick(concept.parent1_id!)}
                >
                  {concept.parent1_id.substring(0, 5)}
                </Badge>
                <Badge
                  variant="secondary"
                  className="cursor-pointer text-xs transition-colors"
                  onClick={() => handleParentClick(concept.parent2_id!)}
                >
                  {concept.parent2_id.substring(0, 5)}
                </Badge>
              </>
            ) : concept.parent1_id ? (
              <>
                <span className="text-xs text-muted-foreground">Parent:</span>
                <Badge
                  variant="secondary"
                  className="cursor-pointer text-xs transition-colors"
                  onClick={() => handleParentClick(concept.parent1_id!)}
                >
                  {concept.parent1_id.substring(0, 5)}
                </Badge>
              </>
            ) : (
              <span className="text-xs text-muted-foreground">
                Initial concept
              </span>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
