import React, { useState } from 'react';
import { CensusSearchForm } from '@/components/CensusSearchForm';
import { CensusResults, CensusDocument } from '@/components/CensusResults';
import { useToast } from '@/components/ui/use-toast';
import { useCensusSearch, useAPIHealth } from '@/hooks/useCensusAPI';
import { type SearchParams } from '@/services/api';
import { APIStatus } from '@/components/APIStatus';
import heroBackground from '@/assets/census-hero-bg.jpg';

const Index = () => {
  const [searchResults, setSearchResults] = useState<CensusDocument[]>([]);
  const [hasSearched, setHasSearched] = useState(false);
  const { toast } = useToast();
  
  // API hooks
  const searchMutation = useCensusSearch();
  const healthQuery = useAPIHealth();

  const handleSearch = async (searchData: SearchParams) => {
    setHasSearched(true);
    
    try {
      const response = await searchMutation.mutateAsync(searchData);
      setSearchResults(response.results);
      
      toast({
        title: "Search Complete",
        description: `Found ${response.total} census documents in ${response.searchTime.toFixed(1)}s`,
      });
    } catch (error) {
      console.error('Search error:', error);
      toast({
        title: "Search Failed",
        description: error instanceof Error ? error.message : "Failed to search census databases. Please try again.",
        variant: "destructive",
      });
    }
  };

  return (
    <>
      <title>Global Census Data Search Engine - Find Census PDFs Worldwide</title>
      <meta 
        name="description" 
        content="Search and download census data PDFs from around the world. Find demographic, migration, and population data by country, year, and region. Free census document discovery tool for researchers."
      />
      
      <div className="min-h-screen">
        {/* API Status */}
        <div className="fixed top-4 right-4 z-50">
          <APIStatus />
        </div>
        
        {/* Hero Section with Background Image */}
        <section 
          className="relative h-[70vh] flex items-center justify-center bg-cover bg-center bg-no-repeat"
          style={{ backgroundImage: `url(${heroBackground})` }}
        >
          {/* Overlay for better text readability */}
          <div className="absolute inset-0 bg-black/10"></div>
          
          {/* Search Form - Centered */}
          <div className="relative z-10 w-full max-w-4xl mx-auto px-4">
            <CensusSearchForm onSearch={handleSearch} isLoading={searchMutation.isPending} />
          </div>
        </section>
        
        {/* Results Section */}
        {hasSearched && (
          <section className="bg-background">
            <div className="container mx-auto px-4 py-8">
              <CensusResults 
                results={searchResults} 
                isLoading={searchMutation.isPending}
                searchTerm=""
              />
            </div>
          </section>
        )}
      </div>
    </>
  );
};

export default Index;
