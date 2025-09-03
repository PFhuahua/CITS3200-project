import React from 'react';
import { useAPIHealth } from '@/hooks/useCensusAPI';
import { Badge } from '@/components/ui/badge';
import { AlertCircle, CheckCircle } from 'lucide-react';

export const APIStatus: React.FC = () => {
  const { data: health, isLoading, error } = useAPIHealth();

  if (isLoading) {
    return (
      <Badge variant="secondary" className="gap-1">
        <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-current"></div>
        Connecting...
      </Badge>
    );
  }

  if (error || !health) {
    return (
      <Badge variant="destructive" className="gap-1">
        <AlertCircle className="h-3 w-3" />
        API Offline
      </Badge>
    );
  }

  return (
    <Badge variant="default" className="gap-1">
      <CheckCircle className="h-3 w-3" />
      API Online
    </Badge>
  );
};
