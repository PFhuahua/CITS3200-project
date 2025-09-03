import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';
import { Download, ExternalLink, FileText, Calendar, MapPin, Building2, ChevronDown, ChevronRight, Folder, FolderOpen } from 'lucide-react';
import { useToast } from '@/components/ui/use-toast';
import { useCensusDownload, useCensusBulkDownload } from '@/hooks/useCensusAPI';

export interface CensusDocument {
  id: string;
  titleEnglish: string;
  titleOriginal?: string;
  country: string;
  province?: string;
  censusYear: number;
  publicationYear: number;
  authorPublisher: string;
  fileSizeMB: number;
  numberOfPages: number;
  volumeNumber?: string;
  fileTypes: string[];
  url: string;
  description?: string;
}

interface CensusResultsProps {
  results: CensusDocument[];
  isLoading?: boolean;
  searchTerm?: string;
}

interface FolderStructure {
  [country: string]: {
    [year: string]: CensusDocument[];
  };
}

export const CensusResults: React.FC<CensusResultsProps> = ({ 
  results, 
  isLoading = false, 
  searchTerm = '' 
}) => {
  const { toast } = useToast();
  const [viewMode, setViewMode] = useState<'folder' | 'table'>('folder');
  const [openFolders, setOpenFolders] = useState<Set<string>>(new Set());
  
  // API hooks
  const downloadMutation = useCensusDownload();
  const bulkDownloadMutation = useCensusBulkDownload();

  // Organize results into folder structure
  const folderStructure: FolderStructure = results.reduce((acc, doc) => {
    if (!acc[doc.country]) {
      acc[doc.country] = {};
    }
    if (!acc[doc.country][doc.censusYear]) {
      acc[doc.country][doc.censusYear] = [];
    }
    acc[doc.country][doc.censusYear].push(doc);
    return acc;
  }, {} as FolderStructure);

  const toggleFolder = (folderId: string) => {
    const newOpenFolders = new Set(openFolders);
    if (newOpenFolders.has(folderId)) {
      newOpenFolders.delete(folderId);
    } else {
      newOpenFolders.add(folderId);
    }
    setOpenFolders(newOpenFolders);
  };

  const handleDownload = async (document: CensusDocument) => {
    try {
      const response = await downloadMutation.mutateAsync(document.id);
      
      // Create a download link
      const link = document.createElement('a');
      link.href = response.download_url;
      link.download = response.filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      toast({
        title: "Download Started",
        description: `Downloading ${document.titleEnglish}`,
      });
    } catch (error) {
      toast({
        title: "Download Failed",
        description: error instanceof Error ? error.message : "Failed to download document",
        variant: "destructive",
      });
    }
  };

  const handleDownloadAll = async () => {
    try {
      const documentIds = results.map(doc => doc.id);
      const blob = await bulkDownloadMutation.mutateAsync(documentIds);
      
      // Create a download link for the ZIP file
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `census_documents_${new Date().toISOString().split('T')[0]}.zip`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      toast({
        title: "Bulk Download Started",
        description: `Downloading ${results.length} documents as ZIP`,
      });
    } catch (error) {
      toast({
        title: "Bulk Download Failed",
        description: error instanceof Error ? error.message : "Failed to download documents",
        variant: "destructive",
      });
    }
  };

  const handleViewSource = (url: string) => {
    window.open(url, '_blank');
  };

  if (isLoading) {
    return (
      <Card className="w-full glass-effect border-0 shadow-xl">
        <CardContent className="p-8">
          <div className="flex items-center justify-center space-x-2">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            <span className="text-lg">Searching census databases...</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (results.length === 0) {
    return (
      <Card className="w-full glass-effect border-0 shadow-xl">
        <CardContent className="p-8 text-center">
          <FileText className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
          <h3 className="text-xl font-semibold mb-2">No Results Found</h3>
          <p className="text-muted-foreground">
            Try adjusting your search criteria or keywords to find census documents.
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="w-full glass-effect border-0 shadow-xl">
      <CardHeader className="flex flex-row items-center justify-between">
        <div>
          <CardTitle className="text-2xl">
            Results ({results.length})
          </CardTitle>
          {searchTerm && (
            <p className="text-muted-foreground mt-1">
              Search results for "{searchTerm}"
            </p>
          )}
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <Button
              variant={viewMode === 'folder' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setViewMode('folder')}
              className="gap-2"
            >
              <Folder className="h-4 w-4" />
              Folder View
            </Button>
            <Button
              variant={viewMode === 'table' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setViewMode('table')}
              className="gap-2"
            >
              <FileText className="h-4 w-4" />
              Table View
            </Button>
          </div>
          <Button
            onClick={handleDownloadAll}
            className="gap-2 census-gradient hover:opacity-90 text-white"
          >
            <Download className="h-4 w-4" />
            Download All PDFs
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        {viewMode === 'folder' ? (
          // Folder Organization View
          <div className="space-y-4">
            {Object.entries(folderStructure).map(([country, years]) => (
              <div key={country} className="border rounded-lg">
                <Collapsible
                  open={openFolders.has(country)}
                  onOpenChange={() => toggleFolder(country)}
                >
                  <CollapsibleTrigger className="flex items-center gap-2 w-full p-4 text-left hover:bg-muted/50 transition-colors">
                    {openFolders.has(country) ? (
                      <FolderOpen className="h-5 w-5 text-primary" />
                    ) : (
                      <Folder className="h-5 w-5 text-muted-foreground" />
                    )}
                    <span className="font-medium text-lg">{country}</span>
                    <span className="text-sm text-muted-foreground ml-auto">
                      {Object.values(years).flat().length} documents
                    </span>
                    {openFolders.has(country) ? (
                      <ChevronDown className="h-4 w-4" />
                    ) : (
                      <ChevronRight className="h-4 w-4" />
                    )}
                  </CollapsibleTrigger>
                  <CollapsibleContent>
                    <div className="px-4 pb-4 space-y-3">
                      {Object.entries(years).map(([year, documents]) => (
                        <div key={`${country}-${year}`} className="ml-6 border-l-2 border-muted pl-4">
                          <Collapsible
                            open={openFolders.has(`${country}-${year}`)}
                            onOpenChange={() => toggleFolder(`${country}-${year}`)}
                          >
                            <CollapsibleTrigger className="flex items-center gap-2 w-full p-2 text-left hover:bg-muted/30 rounded transition-colors">
                              {openFolders.has(`${country}-${year}`) ? (
                                <FolderOpen className="h-4 w-4 text-primary" />
                              ) : (
                                <Folder className="h-4 w-4 text-muted-foreground" />
                              )}
                              <Calendar className="h-4 w-4 text-muted-foreground" />
                              <span className="font-medium">{year}</span>
                              <span className="text-sm text-muted-foreground ml-auto">
                                {documents.length} documents
                              </span>
                              {openFolders.has(`${country}-${year}`) ? (
                                <ChevronDown className="h-3 w-3" />
                              ) : (
                                <ChevronRight className="h-3 w-3" />
                              )}
                            </CollapsibleTrigger>
                            <CollapsibleContent>
                              <div className="ml-6 mt-2 space-y-2">
                                {documents.map((document) => (
                                  <div key={document.id} className="flex items-center justify-between p-3 bg-muted/30 rounded-lg">
                                    <div className="flex-1 min-w-0">
                                      <div className="font-medium text-sm truncate">{document.titleEnglish}</div>
                                      {document.titleOriginal && (
                                        <div className="text-xs text-muted-foreground italic truncate">
                                          {document.titleOriginal}
                                        </div>
                                      )}
                                      <div className="flex items-center gap-4 mt-1">
                                        <span className="text-xs text-muted-foreground">
                                          {document.authorPublisher}
                                        </span>
                                        <span className="text-xs text-muted-foreground">
                                          {document.fileSizeMB.toFixed(1)} MB
                                        </span>
                                        <span className="text-xs text-muted-foreground">
                                          {document.numberOfPages} pages
                                        </span>
                                        {document.volumeNumber && (
                                          <span className="text-xs text-muted-foreground">
                                            {document.volumeNumber}
                                          </span>
                                        )}
                                      </div>
                                      <div className="flex flex-wrap gap-1 mt-1">
                                        {document.fileTypes.map((type) => (
                                          <Badge key={type} variant="secondary" className="text-xs">
                                            {type}
                                          </Badge>
                                        ))}
                                      </div>
                                    </div>
                                    <div className="flex gap-1 ml-3">
                                      <Button
                                        size="sm"
                                        onClick={() => handleDownload(document)}
                                        className="h-7 px-2 text-xs"
                                      >
                                        <Download className="h-3 w-3" />
                                      </Button>
                                      <Button
                                        size="sm"
                                        variant="outline"
                                        onClick={() => handleViewSource(document.url)}
                                        className="h-7 px-2 text-xs"
                                      >
                                        <ExternalLink className="h-3 w-3" />
                                      </Button>
                                    </div>
                                  </div>
                                ))}
                              </div>
                            </CollapsibleContent>
                          </Collapsible>
                        </div>
                      ))}
                    </div>
                  </CollapsibleContent>
                </Collapsible>
              </div>
            ))}
          </div>
        ) : (
          // Table View
          <div className="rounded-lg border overflow-hidden">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Title (English)</TableHead>
                  <TableHead>Original Title</TableHead>
                  <TableHead>Country</TableHead>
                  <TableHead>Province</TableHead>
                  <TableHead>Census Year</TableHead>
                  <TableHead>Publication Year</TableHead>
                  <TableHead>Author/Publisher</TableHead>
                  <TableHead>File Size</TableHead>
                  <TableHead>Pages</TableHead>
                  <TableHead>Volume</TableHead>
                  <TableHead>File Types</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {results.map((document) => (
                  <TableRow key={document.id} className="hover:bg-muted/50">
                    <TableCell className="max-w-xs">
                      <div>
                        <div className="font-medium text-sm">{document.titleEnglish}</div>
                        {document.description && (
                          <div className="text-xs text-muted-foreground mt-1 line-clamp-2">
                            {document.description}
                          </div>
                        )}
                      </div>
                    </TableCell>
                    <TableCell className="max-w-[200px]">
                      {document.titleOriginal ? (
                        <div className="text-sm italic text-muted-foreground truncate">
                          {document.titleOriginal}
                        </div>
                      ) : (
                        <span className="text-muted-foreground text-xs">N/A</span>
                      )}
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-1">
                        <MapPin className="h-3 w-3 text-muted-foreground" />
                        <span className="text-sm">{document.country}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <span className="text-sm">{document.province || 'N/A'}</span>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-1">
                        <Calendar className="h-3 w-3 text-muted-foreground" />
                        <span className="text-sm">{document.censusYear}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <span className="text-sm">{document.publicationYear}</span>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-1">
                        <Building2 className="h-3 w-3 text-muted-foreground" />
                        <span className="text-sm">{document.authorPublisher}</span>
                      </div>
                    </TableCell>
                    <TableCell className="text-sm">{document.fileSizeMB.toFixed(1)} MB</TableCell>
                    <TableCell>{document.numberOfPages}</TableCell>
                    <TableCell>{document.volumeNumber || 'N/A'}</TableCell>
                    <TableCell>
                      <div className="flex flex-wrap gap-1">
                        {document.fileTypes.map((type) => (
                          <Badge key={type} variant="secondary" className="text-xs">
                            {type}
                          </Badge>
                        ))}
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex gap-1">
                        <Button
                          size="sm"
                          onClick={() => handleDownload(document)}
                          className="h-7 px-2 text-xs"
                        >
                          <Download className="h-3 w-3" />
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleViewSource(document.url)}
                          className="h-7 px-2 text-xs"
                        >
                          <ExternalLink className="h-3 w-3" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}
      </CardContent>
    </Card>
  );
};