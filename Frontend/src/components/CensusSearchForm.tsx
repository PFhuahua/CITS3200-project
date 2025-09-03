import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Search, RotateCcw } from 'lucide-react';
import { countries, type CountryData, type StateData } from '@/data/countries';

const searchSchema = z.object({
  year: z.string().optional(),
  country: z.string().optional(),
  state: z.string().optional(),
  keyword: z.string().optional(),
});

type SearchFormData = z.infer<typeof searchSchema>;

interface CensusSearchFormProps {
  onSearch: (data: SearchFormData) => void;
  isLoading?: boolean;
}

export const CensusSearchForm: React.FC<CensusSearchFormProps> = ({ onSearch, isLoading = false }) => {
  const [selectedCountry, setSelectedCountry] = useState<string>('all-countries');
  const [availableStates, setAvailableStates] = useState<StateData[]>([]);

  const form = useForm<SearchFormData>({
    resolver: zodResolver(searchSchema),
    defaultValues: {
      year: 'all-years',
      country: 'all-countries',
      state: 'all-states',
      keyword: '',
    },
  });

  useEffect(() => {
    if (selectedCountry === 'all-countries') {
      setAvailableStates([]);
      return;
    }

    const country = countries.find(c => c.code === selectedCountry);
    if (country?.states) {
      setAvailableStates(country.states);
    } else {
      setAvailableStates([]);
    }
    
    // Reset state selection when country changes
    form.setValue('state', 'all-states');
  }, [selectedCountry, form]);

  const handleSubmit = (data: SearchFormData) => {
    onSearch(data);
  };

  const handleClear = () => {
    form.reset();
    setSelectedCountry('all-countries');
    setAvailableStates([]);
  };

  return (
    <div className="w-full max-w-4xl">
      <Card className="bg-white shadow-xl border-0">
        <CardContent className="p-8">
          <div className="mb-8 text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Global Census Data Search Engine
            </h1>
            <p className="text-lg text-gray-600">
              Search the world's census data by year, country, and state/province. Filter key demographics and export results as a PDF.
            </p>
          </div>
          
          <div className="bg-gray-50 rounded-lg p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">
              Search global census data
            </h2>
            
            <Form {...form}>
              <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                  <FormField
                    control={form.control}
                    name="year"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-sm font-medium text-gray-700">Census year</FormLabel>
                        <Select onValueChange={field.onChange} value={field.value}>
                          <FormControl>
                            <SelectTrigger className="bg-white border-gray-300">
                              <SelectValue placeholder="All years" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent className="bg-white border border-gray-200 shadow-lg max-h-[200px] overflow-auto z-50">
                            <SelectItem value="all-years">All years</SelectItem>
                            <SelectItem value="2024">2024</SelectItem>
                            <SelectItem value="2023">2023</SelectItem>
                            <SelectItem value="2022">2022</SelectItem>
                            <SelectItem value="2021">2021</SelectItem>
                            <SelectItem value="2020">2020</SelectItem>
                            <SelectItem value="2019">2019</SelectItem>
                            <SelectItem value="2018">2018</SelectItem>
                            <SelectItem value="2017">2017</SelectItem>
                            <SelectItem value="2016">2016</SelectItem>
                            <SelectItem value="2015">2015</SelectItem>
                            <SelectItem value="2010">2010</SelectItem>
                            <SelectItem value="2005">2005</SelectItem>
                            <SelectItem value="2000">2000</SelectItem>
                          </SelectContent>
                        </Select>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="country"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-sm font-medium text-gray-700">Country</FormLabel>
                        <Select onValueChange={(value) => {
                          field.onChange(value);
                          setSelectedCountry(value);
                        }} value={field.value}>
                          <FormControl>
                            <SelectTrigger className="bg-white border-gray-300">
                              <SelectValue placeholder="All countries" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent className="bg-white border border-gray-200 shadow-lg max-h-[200px] overflow-auto z-50">
                            <SelectItem value="all-countries">All countries</SelectItem>
                            {countries.map((country) => (
                              <SelectItem key={country.code} value={country.code}>
                                {country.name}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="state"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-sm font-medium text-gray-700">State / Province</FormLabel>
                        <Select 
                          onValueChange={field.onChange} 
                          value={field.value}
                          disabled={selectedCountry === 'all-countries' || availableStates.length === 0}
                        >
                          <FormControl>
                            <SelectTrigger className="bg-white border-gray-300">
                              <SelectValue placeholder={
                                selectedCountry === 'all-countries' 
                                  ? "Select a country first" 
                                  : availableStates.length === 0 
                                    ? "No states available" 
                                    : "All states"
                              } />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent className="bg-white border border-gray-200 shadow-lg max-h-[200px] overflow-auto z-50">
                            <SelectItem value="all-states">All states</SelectItem>
                            {availableStates.map((state) => (
                              <SelectItem key={state.code} value={state.code}>
                                {state.name}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="keyword"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-sm font-medium text-gray-700">Keyword (Optional)</FormLabel>
                        <FormControl>
                          <Input 
                            placeholder="e.g., migration, housing, demographics" 
                            {...field}
                            className="bg-white border-gray-300"
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>

                <div className="flex gap-3 justify-end">
                  <Button
                    type="button"
                    variant="outline"
                    onClick={handleClear}
                    className="px-6 py-2 border-gray-300 text-gray-700 hover:bg-gray-50"
                  >
                    Clear
                  </Button>
                  <Button
                    type="submit"
                    disabled={isLoading}
                    className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white"
                  >
                    {isLoading ? 'Searching...' : 'Search'}
                  </Button>
                </div>
              </form>
            </Form>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};