export interface Filing {
  ticker: string;
  filing_date: string;
  filing_type: string;
  sentiment: {
    positive: number;
    negative: number;
    neutral: number;
  };
  key_metrics: {
    revenue: Array<{
      keyword: string;
      context: string;
      position: number;
    }>;
    expenses: Array<{
      keyword: string;
      context: string;
      position: number;
    }>;
    profit: Array<{
      keyword: string;
      context: string;
      position: number;
    }>;
  };
  financial_values: {
    currency: string[];
    percentage: string[];
    date: string[];
  };
  confidence: number;
  timestamp: string;
}
