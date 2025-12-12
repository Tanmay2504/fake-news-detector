import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { api, type PredictResponse } from '@/lib/api';
import { motion } from 'framer-motion';
import { AlertCircle, CheckCircle, Loader2 } from 'lucide-react';

export function FakeNewsDetector() {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await api.predict({
        text: text.trim(),
        clean: true,
        mode: 'ensemble',
      });
      setResult(response);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze text');
    } finally {
      setLoading(false);
    }
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
          className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-8 mb-8"
        >
          <label className="block mb-4">
            <span className="text-slate-700 dark:text-slate-200 font-semibold block mb-2">
              Enter News Article Text
            </span>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Paste the news article text here..."
              className="w-full h-48 px-4 py-3 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              disabled={loading}
            />
          </label>

          <Button
            type="submit"
            disabled={loading || !text.trim()}
            className="w-full h-12 text-lg font-semibold"
            size="lg"
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                Analyzing...
              </>
            ) : (
              'Analyze Article'
            )}
          </Button>
        </motion.form>

        {error && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6 mb-8"
          >
            <div className="flex items-start">
              <AlertCircle className="h-6 w-6 text-red-600 dark:text-red-400 mr-3 flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="font-semibold text-red-900 dark:text-red-100 mb-1">Error</h3>
                <p className="text-red-700 dark:text-red-300">{error}</p>
              </div>
            </div>
          </motion.div>
        )}

        {result && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            {/* Main Result Card */}
            <div
              className={`rounded-2xl shadow-xl p-8 ${
                isFake
                  ? 'bg-gradient-to-br from-red-50 to-red-100 dark:from-red-950/50 dark:to-red-900/50 border border-red-200 dark:border-red-800'
                  : 'bg-gradient-to-br from-green-50 to-green-100 dark:from-green-950/50 dark:to-green-900/50 border border-green-200 dark:border-green-800'
              }`}
            >
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center">
                  {isFake ? (
                    <AlertCircle className="h-10 w-10 text-red-600 dark:text-red-400 mr-4" />
                  ) : (
                    <CheckCircle className="h-10 w-10 text-green-600 dark:text-green-400 mr-4" />
                  )}
                  <div>
                    <h2 className="text-3xl font-bold capitalize">
                      {result.prediction}
                    </h2>
                    <p className="text-sm text-slate-600 dark:text-slate-400">
                      {result.cached ? 'Cached result' : 'Fresh analysis'}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-4xl font-bold">
                    {(result.confidence * 100).toFixed(1)}%
                  </div>
                  <div className="text-sm text-slate-600 dark:text-slate-400">
                    Confidence
                  </div>
                </div>
              </div>

              {/* Probability Bars */}
              <div className="space-y-3">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="font-medium">Fake News</span>
                    <span>{(result.probability_fake * 100).toFixed(1)}%</span>
                  </div>
                  <div className="h-3 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-red-500 transition-all duration-1000"
                      style={{ width: `${result.probability_fake * 100}%` }}
                    />
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="font-medium">Real News</span>
                    <span>{(result.probability_real * 100).toFixed(1)}%</span>
                  </div>
                  <div className="h-3 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-green-500 transition-all duration-1000"
                      style={{ width: `${result.probability_real * 100}%` }}
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Models Used */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Models Used</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {result.models_used.map((model) => (
                    <Badge key={model} variant="secondary">
                      {model.replace('_', ' ')}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Rule-based Analysis */}
            {result.rule_based_analysis && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Rule-Based Analysis</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <div className="text-sm text-slate-600 dark:text-slate-400 mb-1">
                        Fake Indicators
                      </div>
                      <div className="text-2xl font-bold text-red-600 dark:text-red-400">
                        {result.rule_based_analysis.fake_score}
                      </div>
                    </div>
                    <div>
                      <div className="text-sm text-slate-600 dark:text-slate-400 mb-1">
                        Real Indicators
                      </div>
                      <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                        {result.rule_based_analysis.real_score}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </motion.div>
        )}
      </div>
    </div>
  );
}
