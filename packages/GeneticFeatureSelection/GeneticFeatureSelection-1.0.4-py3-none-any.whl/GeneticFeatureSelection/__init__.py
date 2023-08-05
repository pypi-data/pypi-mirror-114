#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import cross_val_score

class GeneticFeatureSelection:
    def __init__(self):
        pass
    
    def fit(self, X, y):
        self.X = X
        self.y = y
    
    def initialize(self, X, pop_size, heuristic=None):
        self.feats=list(X.columns)
        if heuristic != None:
            missing = [e for e in feats if e not in heuristic]
            idx = [feats.index(m) for m in missing]
            for i in idx:
                heuristic.insert(i, 'empty')

            heuristic_code = [1 if h != 'empty' else 0 for h in heuristic]

            genotype = []
            heuristic_code_copy = heuristic_code.copy()
            for i in [[i for i in idx][:k + 1] for k, j in enumerate(range(len(idx)))]:
                for subi in i:
                    heuristic_code[subi] = 1
                    genotype.append(heuristic_code)
                    heuristic_code = heuristic_code_copy.copy()

        if heuristic == None:            
            genotype = [[np.random.choice([int(0), int(1)]) for i in range(len(X.columns))] for j in range(pop_size * 2)] # initial population
            genotype = [eval(k) for k in list(set([str(g) for g in genotype]))] # remove dups
            genotype = [g for g in genotype if g != [0 for i in range(len(X.columns))]] # remove empty genes
            genotype = genotype[:pop_size]

        Phenotype = [[feat for (code, feat) in zip(gene, X.columns) if code == 1] for gene in genotype] # initial Phenotype
        Phenotype = [p for p in Phenotype if p != []] 

        genotype = [eval(k) for k in list(set([str(g) for g in genotype]))]
        Phenotype = [eval(k) for k in list(set([str(p) for p in Phenotype]))]

        return genotype, Phenotype
    
    def trial(self, population, estimator, X, y, scoring, verbose, cv=5):
        genotype = population[0]
        phenotype = population[1]
        count = 1
        performance = []
        for g, p in zip(genotype, phenotype):
            total = len(genotype)
            fitness = cross_val_score(estimator, X[p], y, cv=cv, scoring=scoring).mean()
            g_str = '-'.join([str(i) for i in g]).replace('.0', '').replace('.1', '')
            if verbose > 1:
                print(f'{count}/{total} | {g_str} | {fitness}')
            performance.append(pd.DataFrame(g + [fitness], index=self.feats + ['Fitness'], dtype='O'))
            count += 1

        performance = pd.concat(performance, axis=1).T
        performance.index = range(len(performance))

        return performance
    
    def selection(self, performance, method, offspring_size):
        performance = performance.copy()
        if (method == 'R' or method == 'RW' or method == 'SUS') and offspring_size == None:
            raise TypeError("'offspring_size' cannot be None if using Rank Selection, Stochastic Universal Sampling or Roulette Wheel Selection.")

        # Roulette Wheel
        if method == 'RW':
            performance['prob'] = performance['Fitness']/sum(performance['Fitness'])
            idx = np.random.choice(performance.index, offspring_size, p=performance['prob'])
            return performance.iloc[idx, :-1]

        # Steady State/Stratify
        if method == 'SS':
            performance.drop_duplicates(inplace=True)
            performance['bin'] = pd.qcut(performance['Fitness'], 3)
            performance = performance.groupby('bin').apply(lambda grp: grp[:2]).reset_index(drop=True)[performance.columns[:-1]]
            return performance

        # Tournament    
        if method == 'T':    
            performance = performance.sample(frac=1)
            performance.index = range(len(performance))
            odd = [i for i in range(len(performance)) if i % 2 == 1]
            even = [i for i in range(len(performance)) if i % 2 == 0]

            winners = []
            for o, e in zip(odd, even):
                if performance.iloc[o, -1] >= performance.iloc[e, -1]:
                     winners.append(performance.iloc[o])

                if performance.iloc[o, -1] < performance.iloc[e, -1]:
                     winners.append(performance.iloc[e])

            winners = pd.concat(winners, axis=1).T

            return winners

        # Stochastic Universal Sampling
        if method == 'SUS':
            sus_index = [np.random.choice(performance.index) for i in range(offspring_size)]
            performance = performance.iloc[sus_index, :]
            return performance

        # Rank  
        if method == 'R':    
            performance = performance.sort_values('Fitness', ascending=False).head(offspring_size)
            return performance
        
    def crossover(self, pairs, pt):
        pairs = pairs.copy()
        pt = int(len(pairs.columns)/pt)

        for i in range(len(pairs.columns)):
            if (i + 1) * pt % 2 != 1 and i < pt - 1:
                pairs[:2].iloc[0, i*pt:(i+1)*pt], pairs[:2].iloc[1, i*pt:(i+1)*pt] = pairs[:2].iloc[1, i*pt:(i+1)*pt], pairs[:2].iloc[0, i*pt:(i+1)*pt]

        return pairs

    def reproduction(self, parents, c_pt, verbose=0):
        parents = parents.copy()
        if 'Fitness' in parents.columns:
            parents.drop('Fitness', axis=1, inplace=True)

        children = []
        for i in range(len(parents)):
            if i != len(parents) - 1:
                children.append(self.crossover(parents[i:i+2], 2))

            if i == len(parents) - 1:
                children.append(self.crossover(parents.iloc[[0, -1], :], 2))

        children = pd.concat(children)
        children.index = range(len(children))

        if verbose > 0:
            print(children[children.columns[:-1]])
        
        if 'Fitness' in children.columns:
            children.drop('Fitness', axis=1, inplace=True)
        
        return children.drop_duplicates()
    
    def mutation(self, offspring, epsilon=.1):
        offspring = offspring.copy()
        # Bit string mutation
        n_mu = 0
        for row in range(len(offspring)):
            col = np.random.choice(len(offspring.columns))
            if epsilon > np.random.random():
                n_mu += 1
                
                if int(offspring.iloc[row, col]) == 0:
                    offspring.iloc[row, col] = 1

                if int(offspring.iloc[row, col]) == 1:
                    offspring.iloc[row, col] = 0
                    
        if n_mu > 0:
            print(f'Mutation Occured! x {n_mu}')
                
        return abs(offspring)
    
    def encode(self, X, population):
        genotype = [population.iloc[i, :].to_list() for i in range(len(population))]
        genotype = [eval(k) for k in list(set([str(g) for g in genotype]))]
        genotype = [[int(k) for k in g] for g in genotype]

        Phenotype = [[feat for (code, feat) in zip(gene, X.columns) if code == 1] for gene in genotype] # initial Phenotype
        Phenotype = [p for p in Phenotype if p != []] 
        Phenotype = [eval(k) for k in list(set([str(p) for p in Phenotype]))]

        return genotype, Phenotype
    
    def sequential_selection(self, pop_size, estimator, scoring, cv, select_method, offspring_size, c_pt, epsilon=.1, heuristic=None, tolerance=5, verbose=1):
        total_start = time.time()
        population = self.initialize(self.X, pop_size, heuristic)
        n_gen = 1
        self.trial_best = []
        self.track = {}
        self.mean_fitness = []
        selection_pressure = 0
        if tolerance == 'auto':
            tolerance = np.inf
       
        while True:
            start = time.time()
            if verbose > 0:
                print(f'---------------------------------------------Gen {n_gen}---------------------------------------------')
            performance = self.trial(population, estimator, self.X, self.y, scoring, verbose, cv=cv)
            individuals = self.selection(performance, select_method, offspring_size)
            self.elite = performance.sort_values('Fitness', ascending=False).drop('Fitness', axis=1).iloc[:int(len(performance)*0.1), :]
            if epsilon == 'adaptive':
                self.elite = performance.sort_values('Fitness', ascending=False).drop('Fitness', axis=1).iloc[:selection_pressure + 5, :]
            self.mean_fitness.append(individuals['Fitness'].mean())
            best_score = performance['Fitness'].sort_values(ascending=False).head(1).values[0]
            self.track[performance['Fitness'].sort_values(ascending=False).iloc[0]] = performance.sort_values('Fitness', ascending=False).drop('Fitness', axis=1).iloc[0].to_dict()
            if verbose >= 1:
                print(f'Mean Fitness: {round(self.mean_fitness[-1], 2)}, Trial Best: {best_score}')
            offspring = self.reproduction(individuals, c_pt, verbose=0)
            population = self.mutation(offspring, epsilon)
            population=pd.concat([population, self.elite])
            population = self.encode(self.X, population)
            self.trial_best.append(best_score)
            
            n_gen += 1
            
            end = time.time()
            time_spent = end - start
            if verbose > 0:
                print(f'Selection Pressure: {selection_pressure} \nTime Spent: {round(time_spent, 2)}') 

            if n_gen > 2:
                if max(self.trial_best) >= self.trial_best[-1]:
                    selection_pressure += 1
                    
                if max(self.trial_best) < self.trial_best[-1]:
                    selection_pressure -= 1
                
                if self.mean_fitness[-1] >= self.trial_best[-1] and tolerance == 'auto':
                    print('Mean fitness has catch up with currrent fitness.')
                    break
                
            if epsilon == 'adaptive':
                epsilon = selection_pressure/10
            
            if selection_pressure > tolerance:
                print('\nThe trial best of this generation shows no improvement.')
                break
        
        
        total_end = time.time()
        total_time_spent = total_end - total_start
        if verbose > 0:
            print(f'\nTotal Time Spent: {round(total_time_spent, 2)}')
        
        sns.set_theme()
        fig, ax = plt.subplots(figsize=(15, 6))  
        plt.plot(self.trial_best, marker='o')
        plt.plot(self.mean_fitness, marker='o')
        plt.axvline(x = np.argmax(gfs.trial_best), color='black', linewidth=2, linestyle='--')
        plt.ylabel('Fitness')
        plt.xlabel('Generations')
        plt.legend(['Trial Best', 'Mean Fitness'])
        title_str = 'neg_mean_absolute_error'.replace('_', ' ').title()
        if 'Neg' in title_str:
            title_str = title_str.replace('Neg', 'Negative')
        plt.title(f'{title_str} of Each Generations')
        plt.show()
        
        self.best_subset = [k for k, v in self.track[np.max(list(self.track.keys()))].items() if int(v) == 1]
        
        print(f'--------------------------------------End of Genetic Feature Selection--------------------------------------')
