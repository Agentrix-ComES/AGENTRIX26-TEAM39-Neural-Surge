import React from 'react';
import { Coffee, Sun, Moon, Sparkles, CheckCircle2, ShoppingBag } from 'lucide-react';

export default function MealDetailCard({ type, meal }) {
  const isBreakfast = type === 'breakfast';
  const isLunch = type === 'lunch';
  
  const Icon = isBreakfast ? Coffee : (isLunch ? Sun : Moon);
  const colorClass = isBreakfast ? 'text-amber-400 bg-amber-500/10 border-amber-500/20' 
                   : (isLunch ? 'text-sky-400 bg-sky-500/10 border-sky-500/20' 
                   : 'text-indigo-400 bg-indigo-500/10 border-indigo-500/20');

  const consumedSet = new Set((meal.inventory_consumed || []).map(i => i.toLowerCase()));

  return (
    <div className="glass rounded-2xl p-6 flex flex-col justify-between border border-slate-800 hover:border-slate-700/80 transition-all duration-300 relative overflow-hidden h-full">
      {/* Top Header Card */}
      <div>
        <div className="flex items-center gap-3 mb-4">
          <div className={`w-10 h-10 rounded-xl flex items-center justify-center border ${colorClass}`}>
            <Icon className="w-5 h-5" />
          </div>
          <div>
            <div className="text-xs text-slate-400 font-semibold uppercase tracking-wider">{type}</div>
            <h4 className="font-bold text-lg text-white leading-tight mt-0.5">{meal.meal_name}</h4>
          </div>
        </div>

        {/* Recipe Summary */}
        <p className="text-sm text-slate-400 leading-relaxed mb-5">{meal.recipe_summary}</p>

        {/* Ingredients Check list */}
        <div className="mb-6">
          <h5 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">Ingredients</h5>
          <div className="flex flex-wrap gap-2">
            {(meal.ingredients_used || []).map((ing, idx) => {
              const inStock = consumedSet.has(ing.toLowerCase());
              return (
                <span 
                   key={idx} 
                   className={`text-xs px-2.5 py-1 rounded-lg font-medium flex items-center gap-1.5 border ${
                    inStock 
                       ? 'bg-emerald-500/10 text-emerald-300 border-emerald-500/20' 
                       : 'bg-rose-500/10 text-rose-300 border-rose-500/20'
                  }`}
                >
                  {inStock ? <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" /> : <ShoppingBag className="w-3.5 h-3.5 text-rose-400" />}
                  {ing}
                </span>
              );
            })}
          </div>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="flex items-center justify-between border-t border-slate-850 pt-4 mt-auto">
        <div>
          <div className="text-[10px] text-slate-500 font-semibold uppercase">Est. Cost</div>
          <div className={`font-bold text-sm ${meal.cost_estimate > 0 ? 'text-amber-400' : 'text-emerald-400'}`}>
            {meal.cost_estimate > 0 ? `LKR ${meal.cost_estimate}` : 'LKR 0 (In Stock)'}
          </div>
        </div>

        <div className="text-right">
          <div className="text-[10px] text-slate-500 font-semibold uppercase flex items-center justify-end gap-1">
            <Sparkles className="w-3 h-3 text-cyan-400" /> Nutrition
          </div>
          <div className="font-bold text-sm text-white">{meal.nutrition_score}/100</div>
        </div>
      </div>
    </div>
  );
}
