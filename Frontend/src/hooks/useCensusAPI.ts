import { useMutation, useQuery } from '@tanstack/react-query';
import { censusAPI, type SearchParams, type SearchResponse } from '@/services/api';
import { CensusDocument } from '@/components/CensusResults';

export const useCensusSearch = () => {
  return useMutation({
    mutationFn: (searchParams: SearchParams) => censusAPI.search(searchParams),
    onError: (error) => {
      console.error('Search failed:', error);
    },
  });
};

export const useCensusDownload = () => {
  return useMutation({
    mutationFn: (documentId: string) => censusAPI.downloadDocument(documentId),
    onError: (error) => {
      console.error('Download failed:', error);
    },
  });
};

export const useCensusBulkDownload = () => {
  return useMutation({
    mutationFn: (documentIds: string[]) => censusAPI.downloadBulk(documentIds),
    onError: (error) => {
      console.error('Bulk download failed:', error);
    },
  });
};

export const useAPIHealth = () => {
  return useQuery({
    queryKey: ['api-health'],
    queryFn: () => censusAPI.healthCheck(),
    refetchInterval: 30000, // Check every 30 seconds
    retry: 3,
  });
};
