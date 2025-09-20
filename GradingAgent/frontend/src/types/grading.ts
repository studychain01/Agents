export interface EssayResponse { 
    essay: string;
    relevance_score: number;
    grammar_score: number;
    structure_score: number;
    depth_score: number;
    final_score: number;
    grade: string;
}

export interface EssayRequest {
    essay: string;
}