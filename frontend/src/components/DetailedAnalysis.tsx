import { useState } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Input } from '@/components/ui/input';
import { api } from '@/lib/api';
import {
  Brain,
  FileText,
  Image as ImageIcon,
  AlertCircle,
  CheckCircle,
  Loader2,
  TrendingUp,
  BarChart3,
  Eye,
  Lightbulb,
  Upload,
  Info,
  Target,
  Layers
} from 'lucide-react';

type AnalysisType = 'text' | 'visual';

export function DetailedAnalysis() {
  const [analysisType, setAnalysisType] = useState<AnalysisType>('text');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Text Analysis State
  const [text, setText] = useState('');
  const [textResult, setTextResult] = useState<any>(null);
  const [limeExplanation, setLimeExplanation] = useState<any>(null);
  
  // Visual Analysis State
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [visualResult, setVisualResult] = useState<any>(null);
  const [context, setContext] = useState({
    event: '',
    location: '',
    date: ''
  });

  const handleTextAnalysis = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      // Get prediction
      const prediction = await api.predict({ text });
      setTextResult(prediction);

      // Get LIME explanation
      try {
        const explanation = await api.explain({ text });
        setLimeExplanation(explanation);
      } catch (err) {
        console.error('Failed to get LIME explanation:', err);
      }
    } catch (err: any) {
      setError(err.message || 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleVisualAnalysis = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) return;

    setError(null);
    setLoading(true);

    try {
      const result = await api.detectVisual(
        selectedFile,
        context.event,
        context.location,
        context.date
      );
      console.log('Visual analysis result:', result);
      setVisualResult(result);
      
      // Scroll to results after a brief delay
      setTimeout(() => {
        const resultsSection = document.getElementById('visual-results');
        if (resultsSection) {
          resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }, 100);
    } catch (err: any) {
      setError(err.message || 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const getTextStats = (text: string) => {
    const words = text.trim().split(/\s+/).filter(Boolean);
    const sentences = text.split(/[.!?]+/).filter(Boolean);
    const avgWordLength = words.reduce((sum, word) => sum + word.length, 0) / words.length || 0;
    const uppercaseWords = words.filter(word => word === word.toUpperCase() && word.length > 1).length;
    const exclamationMarks = (text.match(/!/g) || []).length;
    const questionMarks = (text.match(/\?/g) || []).length;
    
    return {
      wordCount: words.length,
      sentenceCount: sentences.length,
      avgWordLength: avgWordLength.toFixed(1),
      avgWordsPerSentence: (words.length / sentences.length || 0).toFixed(1),
      uppercaseWords,
      exclamationMarks,
      questionMarks
    };
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-slate-100 dark:from-slate-950 dark:via-blue-950 dark:to-slate-900 py-12">
      <div className="container mx-auto px-4">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <div className="flex items-center justify-center gap-3 mb-4">
            <Brain className="h-12 w-12 text-blue-600 dark:text-blue-400" />
            <h1 className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400">
              Detailed Analysis
            </h1>
          </div>
          <p className="text-lg text-slate-600 dark:text-slate-400">
            In-depth analysis with model breakdowns, explanations, and statistics
          </p>
        </motion.div>

        {/* Type Selector */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="flex justify-center gap-4 mb-12"
        >
          <Button
            variant={analysisType === 'text' ? 'default' : 'outline'}
            size="lg"
            onClick={() => setAnalysisType('text')}
            className="gap-2"
          >
            <FileText className="h-5 w-5" />
            Text Analysis
          </Button>
          <Button
            variant={analysisType === 'visual' ? 'default' : 'outline'}
            size="lg"
            onClick={() => setAnalysisType('visual')}
            className="gap-2"
          >
            <ImageIcon className="h-5 w-5" />
            Visual Analysis
          </Button>
        </motion.div>

        {/* Text Analysis */}
        {analysisType === 'text' && (
          <div className="space-y-8">
            {/* Input Form */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
            >
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <FileText className="h-6 w-6" />
                    Enter Article Text
                  </CardTitle>
                  <CardDescription>
                    Paste the full article text for comprehensive analysis
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handleTextAnalysis} className="space-y-4">
                    <Textarea
                      value={text}
                      onChange={(e) => setText(e.target.value)}
                      placeholder="Enter or paste the article text here..."
                      className="min-h-[200px]"
                      disabled={loading}
                    />
                    <Button
                      type="submit"
                      disabled={loading || !text.trim()}
                      className="w-full"
                      size="lg"
                    >
                      {loading ? (
                        <>
                          <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                          Analyzing...
                        </>
                      ) : (
                        <>
                          <Brain className="mr-2 h-5 w-5" />
                          Analyze Text
                        </>
                      )}
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </motion.div>

            {/* Error Display */}
            {error && (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
              >
                <Card className="border-red-200 dark:border-red-800">
                  <CardContent className="pt-6">
                    <div className="flex items-start gap-3">
                      <AlertCircle className="h-6 w-6 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
                      <div>
                        <h3 className="font-semibold text-red-900 dark:text-red-100">Error</h3>
                        <p className="text-red-700 dark:text-red-300">{error}</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            )}

            {/* Text Analysis Results */}
            {textResult && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-6"
              >
                {/* Overall Result */}
                <Card className={`border-2 ${textResult.prediction === 'fake' ? 'border-red-500 dark:border-red-400' : 'border-green-500 dark:border-green-400'}`}>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        {textResult.prediction === 'fake' ? (
                          <AlertCircle className="h-10 w-10 text-red-600 dark:text-red-400" />
                        ) : (
                          <CheckCircle className="h-10 w-10 text-green-600 dark:text-green-400" />
                        )}
                        <div>
                          <CardTitle className="text-3xl capitalize">{textResult.prediction}</CardTitle>
                          <CardDescription className="text-lg mt-1">
                            {(textResult.confidence * 100).toFixed(1)}% confidence
                          </CardDescription>
                        </div>
                      </div>
                      <div className="text-right">
                        <Badge variant={textResult.cached ? 'secondary' : 'outline'}>
                          {textResult.cached ? 'Cached Result' : 'Fresh Analysis'}
                        </Badge>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <div className="text-sm text-slate-600 dark:text-slate-400 mb-2">
                          Fake News Probability
                        </div>
                        <div className="flex items-center gap-3">
                          <div className="flex-1 h-3 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                            <div
                              className="h-full bg-red-500 transition-all duration-1000"
                              style={{ width: `${textResult.probability_fake * 100}%` }}
                            />
                          </div>
                          <span className="text-lg font-semibold min-w-[60px]">
                            {(textResult.probability_fake * 100).toFixed(1)}%
                          </span>
                        </div>
                      </div>
                      <div>
                        <div className="text-sm text-slate-600 dark:text-slate-400 mb-2">
                          Real News Probability
                        </div>
                        <div className="flex items-center gap-3">
                          <div className="flex-1 h-3 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                            <div
                              className="h-full bg-green-500 transition-all duration-1000"
                              style={{ width: `${textResult.probability_real * 100}%` }}
                            />
                          </div>
                          <span className="text-lg font-semibold min-w-[60px]">
                            {(textResult.probability_real * 100).toFixed(1)}%
                          </span>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Text Statistics */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <BarChart3 className="h-6 w-6 text-blue-600 dark:text-blue-400" />
                      Text Statistics
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid md:grid-cols-4 gap-4">
                      {Object.entries(getTextStats(text)).map(([key, value]) => (
                        <div key={key} className="text-center p-4 bg-slate-50 dark:bg-slate-800/50 rounded-lg">
                          <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                            {value}
                          </div>
                          <div className="text-sm text-slate-600 dark:text-slate-400 mt-1">
                            {key.replace(/([A-Z])/g, ' $1').trim()}
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                {/* Individual Model Predictions */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Layers className="h-6 w-6 text-purple-600 dark:text-purple-400" />
                      Individual Model Predictions
                    </CardTitle>
                    <CardDescription>
                      How each ML model voted with their specific probabilities (weighted ensemble)
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {textResult.individual_predictions && Object.entries(textResult.individual_predictions).map(([model, pred]: [string, any]) => {
                        const weights: Record<string, number> = {
                          random_forest: 60,
                          lightgbm: 20,
                          xgboost: 20
                        };
                        const weight = weights[model] || 33;
                        const fakePct = (pred.probability_fake * 100).toFixed(1);
                        const realPct = (pred.probability_real * 100).toFixed(1);
                        
                        return (
                          <div key={model} className="p-4 bg-slate-50 dark:bg-slate-800/50 rounded-lg">
                            <div className="flex items-center justify-between mb-3">
                              <div className="flex items-center gap-2">
                                <Badge variant="secondary" className="text-sm">
                                  {model.replace('_', ' ').toUpperCase()}
                                </Badge>
                                <span className="text-sm text-slate-600 dark:text-slate-400">
                                  Weight: {weight}%
                                </span>
                              </div>
                              <Badge variant={pred.prediction === 'fake' ? 'destructive' : 'success'}>
                                {pred.prediction.toUpperCase()} ({(pred.confidence * 100).toFixed(1)}%)
                              </Badge>
                            </div>
                            
                            <div className="space-y-2">
                              <div>
                                <div className="flex justify-between items-center mb-1">
                                  <span className="text-xs font-medium text-red-700 dark:text-red-400">
                                    Fake Probability
                                  </span>
                                  <span className="text-xs font-bold text-red-600 dark:text-red-400">
                                    {fakePct}%
                                  </span>
                                </div>
                                <div className="h-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                                  <div 
                                    className="h-full bg-red-500 transition-all duration-500"
                                    style={{ width: `${fakePct}%` }}
                                  />
                                </div>
                              </div>
                              
                              <div>
                                <div className="flex justify-between items-center mb-1">
                                  <span className="text-xs font-medium text-green-700 dark:text-green-400">
                                    Real Probability
                                  </span>
                                  <span className="text-xs font-bold text-green-600 dark:text-green-400">
                                    {realPct}%
                                  </span>
                                </div>
                                <div className="h-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                                  <div 
                                    className="h-full bg-green-500 transition-all duration-500"
                                    style={{ width: `${realPct}%` }}
                                  />
                                </div>
                              </div>
                            </div>
                            
                            <div className="mt-3 pt-3 border-t border-slate-200 dark:border-slate-700">
                              <div className="flex justify-between text-xs">
                                <span className="text-slate-600 dark:text-slate-400">
                                  Weighted Contribution:
                                </span>
                                <span className="font-semibold">
                                  Fake: {((pred.probability_fake * weight) / 100).toFixed(3)} | 
                                  Real: {((pred.probability_real * weight) / 100).toFixed(3)}
                                </span>
                              </div>
                            </div>
                          </div>
                        );
                      })}
                      
                      {(!textResult.individual_predictions || Object.keys(textResult.individual_predictions).length === 0) && textResult.models_used.map((model: string) => {
                        const weights: Record<string, number> = {
                          random_forest: 60,
                          lightgbm: 20,
                          xgboost: 20
                        };
                        const weight = weights[model] || 33;
                        
                        return (
                          <div key={model} className="p-4 bg-slate-50 dark:bg-slate-800/50 rounded-lg">
                            <div className="flex items-center justify-between mb-3">
                              <div className="flex items-center gap-2">
                                <Badge variant="secondary">{model.replace('_', ' ')}</Badge>
                                <span className="text-sm text-slate-600 dark:text-slate-400">
                                  Weight: {weight}%
                                </span>
                              </div>
                              <div className="text-sm font-medium">
                                Vote: <span className={textResult.prediction === 'fake' ? 'text-red-600' : 'text-green-600'}>
                                  {textResult.prediction.toUpperCase()}
                                </span>
                              </div>
                            </div>
                            <div className="flex gap-2">
                              <div className="flex-1">
                                <div className="text-xs text-slate-600 dark:text-slate-400 mb-1">Fake</div>
                                <div className="h-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                                  <div 
                                    className="h-full bg-red-500"
                                    style={{ width: `${textResult.probability_fake * 100}%` }}
                                  />
                                </div>
                              </div>
                              <div className="flex-1">
                                <div className="text-xs text-slate-600 dark:text-slate-400 mb-1">Real</div>
                                <div className="h-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                                  <div 
                                    className="h-full bg-green-500"
                                    style={{ width: `${textResult.probability_real * 100}%` }}
                                  />
                                </div>
                              </div>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </CardContent>
                </Card>

                {/* Rule-Based Analysis */}
                {textResult.rule_based_analysis && (
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Target className="h-6 w-6 text-orange-600 dark:text-orange-400" />
                        Rule-Based Pattern Analysis
                      </CardTitle>
                      <CardDescription>
                        Linguistic patterns and indicators detected
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="grid md:grid-cols-2 gap-6">
                        <div className="p-6 bg-red-50 dark:bg-red-950/30 rounded-lg border-2 border-red-200 dark:border-red-800">
                          <div className="flex items-center gap-2 mb-3">
                            <AlertCircle className="h-6 w-6 text-red-600 dark:text-red-400" />
                            <h3 className="font-semibold text-red-900 dark:text-red-100">
                              Fake Indicators
                            </h3>
                          </div>
                          <div className="text-4xl font-bold text-red-600 dark:text-red-400 mb-2">
                            {textResult.rule_based_analysis.fake_score}
                          </div>
                          <div className="text-sm text-red-700 dark:text-red-300">
                            patterns detected
                          </div>
                        </div>
                        
                        <div className="p-6 bg-green-50 dark:bg-green-950/30 rounded-lg border-2 border-green-200 dark:border-green-800">
                          <div className="flex items-center gap-2 mb-3">
                            <CheckCircle className="h-6 w-6 text-green-600 dark:text-green-400" />
                            <h3 className="font-semibold text-green-900 dark:text-green-100">
                              Real Indicators
                            </h3>
                          </div>
                          <div className="text-4xl font-bold text-green-600 dark:text-green-400 mb-2">
                            {textResult.rule_based_analysis.real_score}
                          </div>
                          <div className="text-sm text-green-700 dark:text-green-300">
                            patterns detected
                          </div>
                        </div>
                      </div>
                      
                      <div className="mt-6 p-4 bg-slate-50 dark:bg-slate-800/50 rounded-lg">
                        <div className="flex items-start gap-2">
                          <Info className="h-5 w-5 text-blue-600 dark:text-blue-400 mt-0.5 flex-shrink-0" />
                          <div className="text-sm text-slate-700 dark:text-slate-300">
                            <strong>Common Fake Indicators:</strong> Excessive capitalization, multiple exclamation marks, 
                            sensational language, clickbait phrases, lack of sources, emotional appeals
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                )}

                {/* LIME Explanation */}
                {limeExplanation && (
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Lightbulb className="h-6 w-6 text-yellow-600 dark:text-yellow-400" />
                        LIME Explainability
                      </CardTitle>
                      <CardDescription>
                        Word-level importance for the prediction (top features)
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      {limeExplanation.explanation && limeExplanation.explanation.length > 0 ? (
                        <div className="space-y-3">
                          {limeExplanation.explanation.slice(0, 15).map((item: any, idx: number) => {
                            const [feature, weight] = item;
                            const isPositive = weight > 0;
                            const absWeight = Math.abs(weight);
                            
                            return (
                              <div key={idx} className="flex items-center gap-3">
                                <div className="flex-1 flex items-center gap-2">
                                  <Badge variant={isPositive ? 'destructive' : 'success'}>
                                    {feature}
                                  </Badge>
                                  <div className="flex-1 h-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                                    <div
                                      className={`h-full ${isPositive ? 'bg-red-500' : 'bg-green-500'}`}
                                      style={{ width: `${Math.min(absWeight * 100, 100)}%` }}
                                    />
                                  </div>
                                  <span className={`text-sm font-medium min-w-[80px] text-right ${isPositive ? 'text-red-600' : 'text-green-600'}`}>
                                    {weight > 0 ? '+' : ''}{weight.toFixed(3)}
                                  </span>
                                </div>
                              </div>
                            );
                          })}
                        </div>
                      ) : (
                        <div className="text-center py-8 text-slate-500 dark:text-slate-400">
                          No explanation data available
                        </div>
                      )}
                    </CardContent>
                  </Card>
                )}
              </motion.div>
            )}
          </div>
        )}

        {/* Visual Analysis */}
        {analysisType === 'visual' && (
          <div className="space-y-8">
            {/* Upload Form */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
            >
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <ImageIcon className="h-6 w-6" />
                    Upload Image
                  </CardTitle>
                  <CardDescription>
                    Upload an image for detailed visual analysis
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handleVisualAnalysis} className="space-y-4">
                    {/* File Upload */}
                    <div className="border-2 border-dashed border-slate-300 dark:border-slate-600 rounded-lg p-8 text-center hover:border-blue-500 dark:hover:border-blue-400 transition-colors">
                      <input
                        type="file"
                        accept="image/*"
                        onChange={handleFileSelect}
                        className="hidden"
                        id="file-upload"
                        disabled={loading}
                      />
                      <label htmlFor="file-upload" className="cursor-pointer">
                        {preview ? (
                          <div className="space-y-4">
                            <img
                              src={preview}
                              alt="Preview"
                              className="max-h-64 mx-auto rounded-lg shadow-lg"
                            />
                            <Button type="button" variant="outline" size="sm">
                              Change Image
                            </Button>
                          </div>
                        ) : (
                          <div className="space-y-4">
                            <Upload className="h-16 w-16 mx-auto text-slate-400" />
                            <div>
                              <p className="text-lg font-medium text-slate-700 dark:text-slate-300">
                                Click to upload image
                              </p>
                              <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
                                PNG, JPG, JPEG up to 10MB
                              </p>
                            </div>
                          </div>
                        )}
                      </label>
                    </div>

                    {/* Context Fields */}
                    <div className="grid md:grid-cols-3 gap-4">
                      <div>
                        <label className="text-sm font-medium text-slate-700 dark:text-slate-300 mb-2 block">
                          Event (Optional)
                        </label>
                        <Input
                          placeholder="e.g., Presidential Speech"
                          value={context.event}
                          onChange={(e) => setContext({ ...context, event: e.target.value })}
                          disabled={loading}
                        />
                      </div>
                      <div>
                        <label className="text-sm font-medium text-slate-700 dark:text-slate-300 mb-2 block">
                          Location (Optional)
                        </label>
                        <Input
                          placeholder="e.g., Washington DC"
                          value={context.location}
                          onChange={(e) => setContext({ ...context, location: e.target.value })}
                          disabled={loading}
                        />
                      </div>
                      <div>
                        <label className="text-sm font-medium text-slate-700 dark:text-slate-300 mb-2 block">
                          Date (Optional)
                        </label>
                        <Input
                          placeholder="e.g., 2024-01-15"
                          value={context.date}
                          onChange={(e) => setContext({ ...context, date: e.target.value })}
                          disabled={loading}
                        />
                      </div>
                    </div>

                    <Button
                      type="submit"
                      disabled={loading || !selectedFile}
                      className="w-full"
                      size="lg"
                    >
                      {loading ? (
                        <>
                          <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                          Analyzing...
                        </>
                      ) : (
                        <>
                          <Eye className="mr-2 h-5 w-5" />
                          Analyze Image
                        </>
                      )}
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </motion.div>

            {/* Error Display */}
            {error && (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
              >
                <Card className="border-red-200 dark:border-red-800">
                  <CardContent className="pt-6">
                    <div className="flex items-start gap-3">
                      <AlertCircle className="h-6 w-6 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
                      <div>
                        <h3 className="font-semibold text-red-900 dark:text-red-100">Error</h3>
                        <p className="text-red-700 dark:text-red-300">{error}</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            )}

            {/* Visual Analysis Results */}
            {visualResult && (
              <motion.div
                id="visual-results"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-6"
              >
                {/* Header with Verdict */}
                {(() => {
                  const isAiGenerated = (visualResult.ai_generated_score || 0) > 0.5;
                  const isManipulated = visualResult.manipulation_detected;
                  const isSuspicious = isAiGenerated || isManipulated;
                  const fakeScore = visualResult.final_verdict?.fake_score || 0;
                  
                  let verdictLabel = 'AUTHENTIC';
                  let verdictClass = 'bg-green-500';
                  
                  if (fakeScore >= 70) {
                    verdictLabel = 'SUSPICIOUS';
                    verdictClass = 'bg-red-500';
                  } else if (fakeScore >= 40) {
                    verdictLabel = 'QUESTIONABLE';
                    verdictClass = 'bg-yellow-500';
                  }
                  
                  return (
                    <Card className="border-2 border-blue-500 dark:border-blue-400">
                      <CardHeader className="pb-4">
                        <div className="flex items-center justify-between flex-wrap gap-4">
                          <CardTitle className="text-2xl">Visual Analysis Results</CardTitle>
                          <div className="flex items-center gap-4">
                            <Badge className={`${verdictClass} text-white text-base px-4 py-2`}>
                              {verdictLabel}
                            </Badge>
                            <span className="text-2xl font-bold">
                              {fakeScore.toFixed(2)}% Suspicious
                            </span>
                          </div>
                        </div>
                        {isSuspicious && (
                          <div className="flex items-start gap-2 mt-3 text-yellow-600 dark:text-yellow-400">
                            <AlertCircle className="h-5 w-5 mt-0.5 flex-shrink-0" />
                            <span className="text-sm font-medium">Image authenticity questionable</span>
                          </div>
                        )}
                      </CardHeader>
                      
                      {isSuspicious && (
                        <CardContent className="pt-0 pb-4 border-t border-slate-200 dark:border-slate-700">
                          <div className="space-y-3">
                            <div className="flex items-start gap-2 text-yellow-600 dark:text-yellow-400">
                              <AlertCircle className="h-5 w-5 mt-0.5 flex-shrink-0" />
                              <div>
                                <div className="font-semibold">Recommendation:</div>
                                <div className="text-sm">Verify image authenticity - perform additional verification</div>
                              </div>
                            </div>
                            
                            <div>
                              <div className="font-semibold mb-2">Detection Reasons:</div>
                              <div className="space-y-1.5">
                                {visualResult.final_verdict?.reasons?.map((reason: string, idx: number) => (
                                  <div key={idx} className="flex items-start gap-2 text-sm">
                                    <span className="text-red-500">-</span>
                                    <span>{reason}</span>
                                  </div>
                                ))}
                              </div>
                            </div>
                          </div>
                        </CardContent>
                      )}
                    </Card>
                  );
                })()}
                
                {/* Detection Models Grid */}
                <div className="grid md:grid-cols-3 gap-4">
                  {/* Manipulation Check Card */}
                  {visualResult.manipulation_check && (
                    <Card className="border border-slate-300 dark:border-slate-700">
                      <CardHeader className="pb-3">
                        <div className="flex items-center gap-2">
                          <Eye className="h-5 w-5 text-pink-500" />
                          <CardTitle className="text-base">Manipulation Check</CardTitle>
                        </div>
                      </CardHeader>
                      <CardContent className="space-y-2">
                        <Badge variant={visualResult.manipulation_detected ? 'destructive' : 'success'}>
                          {visualResult.manipulation_detected ? 'Manipulated' : 'Original'}
                        </Badge>
                        <div className="text-sm text-slate-600 dark:text-slate-400">
                          {visualResult.manipulation_check.manipulation_probability !== undefined && (
                            <div>{(visualResult.manipulation_check.manipulation_probability * 100).toFixed(1)}% probability</div>
                          )}
                          <div className="mt-1">Weight: 25%</div>
                        </div>
                      </CardContent>
                    </Card>
                  )}
                  
                  {/* AI Generation Check Card */}
                  {visualResult.ai_generation_check && (
                    <Card className="border border-slate-300 dark:border-slate-700">
                      <CardHeader className="pb-3">
                        <div className="flex items-center gap-2">
                          <Brain className="h-5 w-5 text-blue-500" />
                          <CardTitle className="text-base">AI Generation (CLIP)</CardTitle>
                        </div>
                      </CardHeader>
                      <CardContent className="space-y-2">
                        <Badge variant={visualResult.ai_generation_check.is_ai_generated ? 'destructive' : 'success'}>
                          {visualResult.ai_generation_check.is_ai_generated ? 'AI Generated' : 'Authentic'}
                        </Badge>
                        <div className="text-sm text-slate-600 dark:text-slate-400">
                          {visualResult.ai_generation_check.likely_generator && (
                            <div className="font-medium">{visualResult.ai_generation_check.likely_generator}</div>
                          )}
                          <div>{(visualResult.ai_generation_check.confidence * 100).toFixed(1)}% confidence</div>
                          <div className="mt-1">Weight: 35%</div>
                        </div>
                      </CardContent>
                    </Card>
                  )}
                  
                  {/* Image Content CNN Card */}
                  {visualResult.cnn_prediction && (
                    <Card className="border border-slate-300 dark:border-slate-700">
                      <CardHeader className="pb-3">
                        <div className="flex items-center gap-2">
                          <Layers className="h-5 w-5 text-purple-500" />
                          <CardTitle className="text-base">Image Content (CNN)</CardTitle>
                        </div>
                      </CardHeader>
                      <CardContent className="space-y-2">
                        <Badge variant={visualResult.cnn_prediction.is_fake ? 'destructive' : 'success'}>
                          {visualResult.cnn_prediction.is_fake ? 'FAKE_CONTEXT' : 'REAL_CONTEXT'}
                        </Badge>
                        <div className="text-sm text-slate-600 dark:text-slate-400">
                          <div>CNN (547+2 image classifier)</div>
                          <div>{(visualResult.cnn_prediction.confidence * 100).toFixed(1)}% confidence</div>
                          <div className="mt-1">Weight: 20%</div>
                          <div className="text-xs mt-1 text-slate-500">Trained on 100k images (95.7% accuracy)</div>
                        </div>
                      </CardContent>
                    </Card>
                  )}
                </div>
                
                {/* Context Verification & Content Analysis */}
                <div className="grid md:grid-cols-2 gap-4">
                  {/* Context Verification */}
                  {visualResult.context_verification && (
                    <Card className="border border-slate-300 dark:border-slate-700">
                      <CardHeader className="pb-3">
                        <div className="flex items-center gap-2">
                          <CheckCircle className="h-5 w-5 text-green-500" />
                          <CardTitle className="text-base">Context Verification</CardTitle>
                        </div>
                      </CardHeader>
                      <CardContent className="space-y-2">
                        <div className="text-sm">
                          <div className="font-medium mb-1">BLIP content analysis</div>
                          <div className="text-slate-600 dark:text-slate-400">Weight: 15%</div>
                        </div>
                      </CardContent>
                    </Card>
                  )}
                  
                  {/* Content Analysis */}
                  {visualResult.caption && (
                    <Card className="border border-slate-300 dark:border-slate-700">
                      <CardHeader className="pb-3">
                        <div className="flex items-center gap-2">
                          <FileText className="h-5 w-5 text-blue-500" />
                          <CardTitle className="text-base">Content Analysis</CardTitle>
                        </div>
                      </CardHeader>
                      <CardContent className="space-y-2">
                        <div className="text-sm">
                          <div className="italic mb-2">"{visualResult.caption}"</div>
                          <div className="text-slate-600 dark:text-slate-400">Local BLIP + OpenCV</div>
                        </div>
                      </CardContent>
                    </Card>
                  )}
                </div>
                
                {/* What's in the Image */}
                {(visualResult.caption || visualResult.description) && (
                  <Card className="border border-slate-300 dark:border-slate-700">
                    <CardHeader className="pb-3">
                      <div className="flex items-center gap-2">
                        <ImageIcon className="h-5 w-5 text-yellow-500" />
                        <CardTitle className="text-base">What's in the Image</CardTitle>
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      {visualResult.caption && (
                        <div className="flex items-center justify-between p-3 bg-slate-50 dark:bg-slate-800/50 rounded">
                          <span className="text-sm">{visualResult.caption}</span>
                          <Badge variant="secondary">100%</Badge>
                        </div>
                      )}
                      
                      {visualResult.description && visualResult.description !== visualResult.caption && (
                        <div className="p-3 bg-blue-50 dark:bg-blue-950/30 rounded border border-blue-200 dark:border-blue-800">
                          <div className="text-xs font-semibold text-blue-600 dark:text-blue-400 mb-1">
                            Detailed Description
                          </div>
                          <p className="text-sm text-slate-700 dark:text-slate-300">{visualResult.description}</p>
                        </div>
                      )}
                      
                      {visualResult.detected_objects && visualResult.detected_objects.length > 0 && (
                        <div>
                          <div className="text-sm font-semibold mb-2">Objects Detected:</div>
                          <div className="flex flex-wrap gap-2">
                            {visualResult.detected_objects.map((obj: any, idx: number) => (
                              <Badge key={idx} variant="outline">
                                {typeof obj === 'string' ? obj : obj.name} 
                                {obj.confidence && ` (${(obj.confidence * 100).toFixed(0)}%)`}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      )}
                      
                      {/* Google Vision Labels */}
                      {visualResult.labels && visualResult.labels.length > 0 && (
                        <div>
                          <div className="text-sm font-semibold mb-2">Google Vision Labels:</div>
                          <div className="flex flex-wrap gap-2">
                            {visualResult.labels.map((label: any, idx: number) => {
                              const description = typeof label === 'string' ? label : (label.description || label.name);
                              const score = typeof label === 'object' && label.score ? (label.score * 100).toFixed(0) : null;
                              
                              return (
                                <Badge key={idx} variant="outline" className="text-xs">
                                  {description}
                                  {score && <span className="ml-1 text-blue-600 dark:text-blue-400">({score}%)</span>}
                                </Badge>
                              );
                            })}
                          </div>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                )}
                
                {/* Face Analysis */}
                {visualResult.faces_detected !== undefined && (
                  <Card className="border border-slate-300 dark:border-slate-700">
                    <CardHeader className="pb-3">
                      <div className="flex items-center gap-2">
                        <Eye className="h-5 w-5 text-orange-500" />
                        <CardTitle className="text-base">Face Analysis</CardTitle>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="text-sm">
                        Faces detected: <strong>{visualResult.faces_detected}</strong>
                      </div>
                    </CardContent>
                  </Card>
                )}
                
                {/* Additional Analysis Details */}
                {(visualResult.manipulation_check?.warning_signs || 
                  visualResult.ai_generation_check?.details || 
                  visualResult.context_verification?.analysis) && (
                  <Card className="border border-slate-300 dark:border-slate-700">
                    <CardHeader className="pb-3">
                      <CardTitle className="text-base">Additional Analysis Details</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      {visualResult.manipulation_check?.warning_signs && 
                       visualResult.manipulation_check.warning_signs.length > 0 && (
                        <div>
                          <div className="text-sm font-semibold mb-2 text-red-600 dark:text-red-400">
                            ⚠️ Manipulation Warning Signs:
                          </div>
                          <ul className="list-disc list-inside space-y-1">
                            {visualResult.manipulation_check.warning_signs.map((sign: string, idx: number) => (
                              <li key={idx} className="text-sm text-slate-700 dark:text-slate-300">{sign}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                      
                      {visualResult.ai_generation_check?.details && (
                        <div>
                          <div className="text-sm font-semibold mb-2 text-blue-600 dark:text-blue-400">
                            🤖 AI Generation Details:
                          </div>
                          <p className="text-sm text-slate-700 dark:text-slate-300">
                            {visualResult.ai_generation_check.details}
                          </p>
                        </div>
                      )}
                      
                      {visualResult.context_verification?.analysis && (
                        <div>
                          <div className="text-sm font-semibold mb-2 text-purple-600 dark:text-purple-400">
                            📋 Context Verification:
                          </div>
                          <p className="text-sm text-slate-700 dark:text-slate-300">
                            {visualResult.context_verification.analysis}
                          </p>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                )}
                
                {/* Image Technical Details */}
                {(visualResult.image_dimensions || visualResult.file_size || visualResult.format) && (
                  <Card className="border border-slate-300 dark:border-slate-700">
                    <CardHeader className="pb-3">
                      <div className="flex items-center gap-2">
                        <Info className="h-5 w-5 text-slate-500" />
                        <CardTitle className="text-base">Image Technical Details</CardTitle>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                        {visualResult.image_dimensions && (
                          <div>
                            <div className="text-slate-600 dark:text-slate-400 mb-1">Dimensions</div>
                            <div className="font-medium">{visualResult.image_dimensions}</div>
                          </div>
                        )}
                        {visualResult.file_size && (
                          <div>
                            <div className="text-slate-600 dark:text-slate-400 mb-1">File Size</div>
                            <div className="font-medium">{visualResult.file_size}</div>
                          </div>
                        )}
                        {visualResult.format && (
                          <div>
                            <div className="text-slate-600 dark:text-slate-400 mb-1">Format</div>
                            <div className="font-medium">{visualResult.format}</div>
                          </div>
                        )}
                        {visualResult.color_mode && (
                          <div>
                            <div className="text-slate-600 dark:text-slate-400 mb-1">Color Mode</div>
                            <div className="font-medium">{visualResult.color_mode}</div>
                          </div>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                )}

                {/* Image Preview */}
                {preview && (
                  <Card className="border border-slate-300 dark:border-slate-700">
                    <CardHeader>
                      <CardTitle>Analyzed Image</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <img
                        src={preview}
                        alt="Analyzed"
                        className="max-w-full h-auto rounded-lg shadow-lg mx-auto"
                      />
                    </CardContent>
                  </Card>
                )}

                {/* Context Information Provided */}
                {(context.event || context.location || context.date) && (
                  <Card className="border border-slate-300 dark:border-slate-700">
                    <CardHeader className="pb-3">
                      <div className="flex items-center gap-2">
                        <Info className="h-5 w-5 text-purple-600 dark:text-purple-400" />
                        <CardTitle className="text-base">Context Provided</CardTitle>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="grid md:grid-cols-3 gap-4 text-sm">
                        {context.event && (
                          <div>
                            <div className="text-slate-600 dark:text-slate-400 mb-1">Event</div>
                            <div className="font-medium">{context.event}</div>
                          </div>
                        )}
                        {context.location && (
                          <div>
                            <div className="text-slate-600 dark:text-slate-400 mb-1">Location</div>
                            <div className="font-medium">{context.location}</div>
                          </div>
                        )}
                        {context.date && (
                          <div>
                            <div className="text-slate-600 dark:text-slate-400 mb-1">Date</div>
                            <div className="font-medium">{context.date}</div>
                          </div>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                )}

                {/* Raw Data */}
                <Card className="border border-slate-300 dark:border-slate-700">
                  <CardContent className="pt-6">
                    <details className="cursor-pointer">
                      <summary className="font-medium text-slate-700 dark:text-slate-300 flex items-center gap-2">
                        <span>▶ View Raw Visual Analysis Data</span>
                      </summary>
                      <pre className="mt-4 p-4 bg-slate-50 dark:bg-slate-900 rounded-lg text-xs overflow-auto max-h-96 border border-slate-200 dark:border-slate-700">
                        {JSON.stringify(visualResult, null, 2)}
                      </pre>
                    </details>
                  </CardContent>
                </Card>
              </motion.div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
