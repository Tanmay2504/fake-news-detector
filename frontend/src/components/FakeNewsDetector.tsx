import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Textarea } from '@/components/ui/textarea';
import { api, type PredictResponse } from '@/lib/api';
import { motion } from 'framer-motion';
import { AlertCircle, CheckCircle, Loader2, Brain, BarChart3, Lightbulb, FileText, TrendingUp } from 'lucide-react';

export function FakeNewsDetector() {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [limeExplanation, setLimeExplanation] = useState<any>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);
    setLimeExplanation(null);

    try {
      // Get prediction
      const response = await api.predict({
        text: text.trim(),
        clean: true,
        mode: 'ensemble',
      });
      setResult(response);

      // Get LIME explanation
      try {
        const explanation = await api.explain({ text: text.trim() });
        setLimeExplanation(explanation);
      } catch (explainErr) {
        console.warn('LIME explanation failed:', explainErr);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze text');
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

  const isFake = result?.prediction === 'fake';

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-950 dark:to-slate-900 py-12 px-4">
      <div className="container mx-auto max-w-4xl">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-5xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-slate-900 to-slate-600 dark:from-white dark:to-slate-300">
            Fake News Detector
          </h1>
          <p className="text-slate-600 dark:text-slate-400 text-lg">
            Advanced AI-powered analysis using ensemble machine learning
          </p>
        </motion.div>

        <motion.form
          onSubmit={handleSubmit}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="space-y-6"
        >
          <Card>
            <CardHeader>
              <CardTitle>Enter News Article Text</CardTitle>
              <CardDescription>
                Paste any news article text to analyze its credibility
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Paste the news article text here..."
                className="min-h-[200px] text-base"
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
                    <FileText className="mr-2 h-5 w-5" />
                    Analyze Article
                  </>
                )}
              </Button>
            </CardContent>
          </Card>
        </motion.form>

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

        {result && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6 mt-6"
          >
            {/* Text Statistics */}
            {(() => {
              const stats = getTextStats(text);
              return (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <BarChart3 className="h-6 w-6 text-blue-600 dark:text-blue-400" />
                      Text Statistics
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div className="text-center p-3 bg-blue-50 dark:bg-blue-950/30 rounded-lg">
                        <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">{stats.wordCount}</div>
                        <div className="text-sm text-slate-600 dark:text-slate-400">Words</div>
                      </div>
                      <div className="text-center p-3 bg-green-50 dark:bg-green-950/30 rounded-lg">
                        <div className="text-2xl font-bold text-green-600 dark:text-green-400">{stats.sentenceCount}</div>
                        <div className="text-sm text-slate-600 dark:text-slate-400">Sentences</div>
                      </div>
                      <div className="text-center p-3 bg-purple-50 dark:bg-purple-950/30 rounded-lg">
                        <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">{stats.avgWordLength}</div>
                        <div className="text-sm text-slate-600 dark:text-slate-400">Avg Word Length</div>
                      </div>
                      <div className="text-center p-3 bg-orange-50 dark:bg-orange-950/30 rounded-lg">
                        <div className="text-2xl font-bold text-orange-600 dark:text-orange-400">{stats.avgWordsPerSentence}</div>
                        <div className="text-sm text-slate-600 dark:text-slate-400">Words/Sentence</div>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-3 gap-4 mt-4">
                      <div className="text-center p-3 bg-slate-50 dark:bg-slate-800/50 rounded-lg">
                        <div className="text-xl font-bold">{stats.uppercaseWords}</div>
                        <div className="text-xs text-slate-600 dark:text-slate-400">Uppercase Words</div>
                      </div>
                      <div className="text-center p-3 bg-slate-50 dark:bg-slate-800/50 rounded-lg">
                        <div className="text-xl font-bold">{stats.exclamationMarks}</div>
                        <div className="text-xs text-slate-600 dark:text-slate-400">Exclamation Marks</div>
                      </div>
                      <div className="text-center p-3 bg-slate-50 dark:bg-slate-800/50 rounded-lg">
                        <div className="text-xl font-bold">{stats.questionMarks}</div>
                        <div className="text-xs text-slate-600 dark:text-slate-400">Question Marks</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              );
            })()}

            {/* Main Prediction Result */}
            <Card className={`border-2 ${result.prediction === 'fake' ? 'border-red-500 dark:border-red-400' : 'border-green-500 dark:border-green-400'}`}>
              <CardHeader>
                <div className="flex items-center justify-between flex-wrap gap-4">
                  <div className="flex items-center gap-3">
                    {result.prediction === 'fake' ? (
                      <AlertCircle className="h-10 w-10 text-red-600 dark:text-red-400" />
                    ) : (
                      <CheckCircle className="h-10 w-10 text-green-600 dark:text-green-400" />
                    )}
                    <div>
                      <CardTitle className="text-3xl capitalize">{result.prediction} News</CardTitle>
                      <CardDescription className="text-lg mt-1">
                        Confidence: {(result.confidence * 100).toFixed(1)}%
                      </CardDescription>
                    </div>
                  </div>
                  <Badge 
                    variant={result.prediction === 'fake' ? 'destructive' : 'success'}
                    className="text-lg px-4 py-2"
                  >
                    {result.cached ? '🔄 Cached' : '✨ Fresh'}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div>
                    <div className="flex justify-between text-sm mb-1 font-medium">
                      <span>Fake Probability</span>
                      <span className="text-red-600 dark:text-red-400">{(result.probability_fake * 100).toFixed(1)}%</span>
                    </div>
                    <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-red-500 transition-all duration-1000"
                        style={{ width: `${result.probability_fake * 100}%` }}
                      />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1 font-medium">
                      <span>Real Probability</span>
                      <span className="text-green-600 dark:text-green-400">{(result.probability_real * 100).toFixed(1)}%</span>
                    </div>
                    <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-green-500 transition-all duration-1000"
                        style={{ width: `${result.probability_real * 100}%` }}
                      />
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Individual Model Predictions */}
            {result.individual_predictions && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Brain className="h-6 w-6 text-purple-600 dark:text-purple-400" />
                    Individual Model Predictions
                  </CardTitle>
                  <CardDescription>
                    Breakdown of each ML model's prediction with weighted contribution
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid md:grid-cols-3 gap-4">
                    {Object.entries(result.individual_predictions).map(([model, prediction]: [string, any]) => {
                      const weight = model === 'random_forest' ? 0.6 : model === 'lightgbm' ? 0.2 : 0.2;
                      const contribution = weight * (prediction.prediction === 'fake' ? prediction.probability_fake : prediction.probability_real);
                      
                      return (
                        <div key={model} className="p-4 bg-slate-50 dark:bg-slate-800/50 rounded-lg border border-slate-200 dark:border-slate-700">
                          <div className="flex items-center justify-between mb-3">
                            <h4 className="font-semibold capitalize">{model.replace('_', ' ')}</h4>
                            <Badge variant="outline">{(weight * 100).toFixed(0)}% weight</Badge>
                          </div>
                          
                          <div className="space-y-2 mb-3">
                            <div className="flex justify-between text-sm">
                              <span className="text-slate-600 dark:text-slate-400">Fake:</span>
                              <span className="font-medium text-red-600 dark:text-red-400">
                                {(prediction.probability_fake * 100).toFixed(1)}%
                              </span>
                            </div>
                            <div className="flex justify-between text-sm">
                              <span className="text-slate-600 dark:text-slate-400">Real:</span>
                              <span className="font-medium text-green-600 dark:text-green-400">
                                {(prediction.probability_real * 100).toFixed(1)}%
                              </span>
                            </div>
                          </div>
                          
                          <div className="pt-3 border-t border-slate-200 dark:border-slate-700">
                            <div className="text-xs text-slate-600 dark:text-slate-400 mb-1">Weighted Contribution</div>
                            <div className="flex items-center gap-2">
                              <div className="flex-1 h-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                                <div
                                  className={`h-full ${prediction.prediction === 'fake' ? 'bg-red-500' : 'bg-green-500'}`}
                                  style={{ width: `${contribution * 100}%` }}
                                />
                              </div>
                              <span className="text-xs font-medium">{(contribution * 100).toFixed(1)}%</span>
                            </div>
                          </div>
                          
                          <Badge 
                            variant={prediction.prediction === 'fake' ? 'destructive' : 'success'}
                            className="w-full justify-center mt-3"
                          >
                            Predicts: {prediction.prediction}
                          </Badge>
                        </div>
                      );
                    })}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* LIME Explanation */}
            {limeExplanation && limeExplanation.word_importances && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Lightbulb className="h-6 w-6 text-yellow-600 dark:text-yellow-400" />
                    AI Explainability (LIME Analysis)
                  </CardTitle>
                  <CardDescription>
                    Words highlighted by their influence on the prediction. Red indicates fake, green indicates real.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="p-4 bg-slate-50 dark:bg-slate-900 rounded-lg">
                    <div className="flex flex-wrap gap-1 text-base leading-relaxed">
                      {limeExplanation.word_importances.map((item: any, idx: number) => {
                        const importance = Math.abs(item.importance);
                        const isFakeIndicator = item.importance > 0;
                        const opacity = Math.min(importance * 3, 1);
                        
                        return (
                          <span
                            key={idx}
                            className="px-1 py-0.5 rounded transition-all hover:scale-110"
                            style={{
                              backgroundColor: isFakeIndicator 
                                ? `rgba(239, 68, 68, ${opacity * 0.3})`
                                : `rgba(34, 197, 94, ${opacity * 0.3})`,
                              fontWeight: importance > 0.05 ? 'bold' : 'normal'
                            }}
                            title={`Importance: ${item.importance.toFixed(3)} (${isFakeIndicator ? 'Fake' : 'Real'} indicator)`}
                          >
                            {item.word}
                          </span>
                        );
                      })}
                    </div>
                    
                    <div className="mt-4 flex items-center justify-center gap-6 text-sm">
                      <div className="flex items-center gap-2">
                        <div className="w-4 h-4 rounded bg-red-500/30"></div>
                        <span className="text-slate-600 dark:text-slate-400">Fake Indicators</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <div className="w-4 h-4 rounded bg-green-500/30"></div>
                        <span className="text-slate-600 dark:text-slate-400">Real Indicators</span>
                      </div>
                    </div>
                  </div>
                  
                  {limeExplanation.top_features && (
                    <div className="mt-4 grid md:grid-cols-2 gap-4">
                      <div>
                        <h4 className="font-semibold mb-2 text-red-600 dark:text-red-400">Top Fake Indicators</h4>
                        <div className="space-y-1">
                          {limeExplanation.top_features
                            .filter((f: any) => f.importance > 0)
                            .slice(0, 5)
                            .map((feature: any, idx: number) => (
                              <div key={idx} className="flex items-center gap-2 text-sm">
                                <span className="font-medium">{feature.word}</span>
                                <div className="flex-1 h-2 bg-red-100 dark:bg-red-950 rounded-full overflow-hidden">
                                  <div
                                    className="h-full bg-red-500"
                                    style={{ width: `${(feature.importance / limeExplanation.top_features[0].importance) * 100}%` }}
                                  />
                                </div>
                                <span className="text-xs text-slate-600 dark:text-slate-400">
                                  {feature.importance.toFixed(3)}
                                </span>
                              </div>
                            ))}
                        </div>
                      </div>
                      
                      <div>
                        <h4 className="font-semibold mb-2 text-green-600 dark:text-green-400">Top Real Indicators</h4>
                        <div className="space-y-1">
                          {limeExplanation.top_features
                            .filter((f: any) => f.importance < 0)
                            .slice(0, 5)
                            .map((feature: any, idx: number) => (
                              <div key={idx} className="flex items-center gap-2 text-sm">
                                <span className="font-medium">{feature.word}</span>
                                <div className="flex-1 h-2 bg-green-100 dark:bg-green-950 rounded-full overflow-hidden">
                                  <div
                                    className="h-full bg-green-500"
                                    style={{ width: `${(Math.abs(feature.importance) / Math.abs(limeExplanation.top_features[limeExplanation.top_features.length - 1].importance)) * 100}%` }}
                                  />
                                </div>
                                <span className="text-xs text-slate-600 dark:text-slate-400">
                                  {Math.abs(feature.importance).toFixed(3)}
                                </span>
                              </div>
                            ))}
                        </div>
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            )}

            {/* Rule-based Analysis */}
            {result.rule_based_analysis && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <TrendingUp className="h-6 w-6 text-orange-600 dark:text-orange-400" />
                    Rule-Based Analysis
                  </CardTitle>
                  <CardDescription>
                    Pattern-based detection using linguistic markers
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid md:grid-cols-2 gap-6">
                    <div className="p-4 bg-red-50 dark:bg-red-950/30 rounded-lg">
                      <div className="text-sm text-slate-600 dark:text-slate-400 mb-1">Fake Indicators</div>
                      <div className="text-3xl font-bold text-red-600 dark:text-red-400">
                        {result.rule_based_analysis.fake_score}
                      </div>
                    </div>
                    <div className="p-4 bg-green-50 dark:bg-green-950/30 rounded-lg">
                      <div className="text-sm text-slate-600 dark:text-slate-400 mb-1">Real Indicators</div>
                      <div className="text-3xl font-bold text-green-600 dark:text-green-400">
                        {result.rule_based_analysis.real_score}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Models Used */}
            <Card>
              <CardHeader>
                <CardTitle>Ensemble Models Used</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {result.models_used.map((model) => (
                    <Badge key={model} variant="secondary" className="text-sm">
                      {model.replace('_', ' ')}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </div>
    </div>
  );
}

