export interface ConceptResponse {
  id: string;
  content: string;
  parent1_id: string | null;
  parent2_id: string | null;
  dream_id: string;
  created_at: string;
}
