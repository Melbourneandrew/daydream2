import { useState, useEffect, useRef, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Button } from "@/components/ui/button";
import { ChevronDownIcon } from "lucide-react";

interface DreamSummary {
  id: string;
  created_at: string;
  label: string;
}

interface DreamListResponse {
  dreams: DreamSummary[];
  has_more: boolean;
  total_count: number;
}

export default function FindDreamsDropdown() {
  const navigate = useNavigate();
  const [dreams, setDreams] = useState<DreamSummary[]>([]);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const loadMoreRef = useRef<HTMLDivElement>(null);

  const ITEMS_PER_PAGE = 20;

  const fetchDreams = useCallback(
    async (offset: number = 0, reset: boolean = false) => {
      if (loading) return;

      setLoading(true);
      setError(null);

      try {
        const response = await fetch(
          `http://localhost:8000/v1/dream/list?offset=${offset}&limit=${ITEMS_PER_PAGE}`
        );

        if (!response.ok) {
          throw new Error(`Failed to fetch dreams: ${response.statusText}`);
        }

        const data: DreamListResponse = await response.json();

        setDreams((prev) => (reset ? data.dreams : [...prev, ...data.dreams]));
        setHasMore(data.has_more);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load dreams");
      } finally {
        setLoading(false);
      }
    },
    [loading]
  );

  // Load initial dreams when dropdown opens
  useEffect(() => {
    if (isDropdownOpen && dreams.length === 0) {
      fetchDreams(0, true);
    }
  }, [isDropdownOpen, dreams.length, fetchDreams]);

  // Infinite scroll implementation
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        const [entry] = entries;
        if (entry.isIntersecting && hasMore && !loading) {
          fetchDreams(dreams.length);
        }
      },
      { threshold: 0.1 }
    );

    const currentLoadMoreRef = loadMoreRef.current;
    if (currentLoadMoreRef) {
      observer.observe(currentLoadMoreRef);
    }

    return () => {
      if (currentLoadMoreRef) {
        observer.unobserve(currentLoadMoreRef);
      }
    };
  }, [dreams.length, hasMore, loading, fetchDreams]);

  const handleDreamSelect = (dreamId: string) => {
    navigate(`/dream/${dreamId}`);
    setIsDropdownOpen(false);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <DropdownMenu open={isDropdownOpen} onOpenChange={setIsDropdownOpen}>
      <DropdownMenuTrigger asChild>
        <Button
          variant="ghost"
          size="sm"
          className="h-9 px-4 py-2 text-sm font-medium focus:outline-none focus:ring-0 focus-visible:ring-0 border-0 cursor-pointer text-foreground"
        >
          Find Dreams
          <ChevronDownIcon
            className={`h-4 w-4 transition-transform duration-200 ${
              isDropdownOpen ? "rotate-180" : ""
            }`}
          />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent
        className="find-dreams-dropdown w-80 max-h-80 overflow-x-hidden"
        align="start"
      >
        {error && <div className="px-2 py-1 text-sm text-red-500">{error}</div>}

        <div
          ref={scrollContainerRef}
          className="find-dreams-scroll max-h-64 overflow-y-auto overflow-x-hidden"
        >
          {dreams.length === 0 && !loading && !error ? (
            <div className="px-2 py-4 text-sm text-muted-foreground text-center">
              No dreams found
            </div>
          ) : (
            dreams.map((dream) => (
              <DropdownMenuItem
                key={dream.id}
                onClick={() => handleDreamSelect(dream.id)}
                className="flex flex-col items-start py-2 px-2 cursor-pointer"
              >
                <div className="font-medium text-sm truncate w-full">
                  {dream.label}
                </div>
                <div className="text-xs text-muted-foreground">
                  {formatDate(dream.created_at)}
                </div>
              </DropdownMenuItem>
            ))
          )}

          {loading && (
            <div className="px-2 py-2 text-sm text-muted-foreground text-center">
              Loading...
            </div>
          )}

          {hasMore && !loading && dreams.length > 0 && (
            <div ref={loadMoreRef} className="h-4" />
          )}

          {!hasMore && dreams.length > 0 && (
            <>
              <DropdownMenuSeparator />
              <div className="px-2 py-2 text-xs text-muted-foreground text-center">
                All dreams loaded
              </div>
            </>
          )}
        </div>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
