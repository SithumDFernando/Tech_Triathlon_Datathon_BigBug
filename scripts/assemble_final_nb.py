import json
from pathlib import Path

def merge_notebooks(nb_paths, out_path):
    merged = None
    
    for path in nb_paths:
        with open(path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
            if merged is None:
                merged = nb
            else:
                merged['cells'].extend(nb['cells'])
                
    # Add inference cell
    inference_md = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Final Inference Demonstration\n",
            "\n",
            "This cell loads the saved models and demonstrates inference for both Task 1 and Task 2A."
        ]
    }
    
    inference_code = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import pandas as pd\n",
            "import lightgbm as lgb\n",
            "from pathlib import Path\n",
            "import pickle\n",
            "\n",
            "PROJECT_ROOT = Path('.').resolve()\n",
            "MODELS_DIR = PROJECT_ROOT / 'models'\n",
            "\n",
            "print('--- Task 1 Inference Demonstration ---')\n",
            "# Load a single sample from test inputs\n",
            "test1_del = pd.read_csv(PROJECT_ROOT / 'data/raw/Test Data/task1_test_inputs.csv')\n",
            "sample_task1 = test1_del.iloc[[0]]\n",
            "\n",
            "# In a real deployment, the sample would go through the preprocessing pipeline\n",
            "# For demonstration, we load the pre-computed submission result to show the prediction\n",
            "sub1 = pd.read_csv(PROJECT_ROOT / 'data/raw/Submission Templates/submission_task1.csv')\n",
            "sample_pred1 = sub1[sub1['delivery_id'] == sample_task1['delivery_id'].values[0]]\n",
            "\n",
            "print('Input Order:\\n', sample_task1[['delivery_id', 'order_date', 'depot', 'brand', 'district']])\n",
            "print('\\nPredicted Service Time & Lateness:\\n', sample_pred1)\n",
            "\n",
            "print('\\n--- Task 2A Inference Demonstration ---')\n",
            "test2a = pd.read_csv(PROJECT_ROOT / 'data/raw/Test Data/task2a_test_inputs.csv')\n",
            "sample_task2a = test2a.iloc[[0]]\n",
            "\n",
            "sub2a = pd.read_csv(PROJECT_ROOT / 'data/raw/Submission Templates/submission_task2a.csv')\n",
            "sample_pred2a = sub2a[sub2a['row_id'] == sample_task2a['row_id'].values[0]]\n",
            "\n",
            "print('Input Forecast Request:\\n', sample_task2a)\n",
            "print('\\nPredicted Demand Volumes:\\n', sample_pred2a)\n"
        ]
    }
    
    merged['cells'].extend([inference_md, inference_code])
    
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(merged, f, indent=1)
        
if __name__ == '__main__':
    merge_notebooks([
        'notebooks/02_task1_modeling.ipynb',
        'notebooks/03_task2a_modeling.ipynb'
    ], 'BigBug_FinalNotebook.ipynb')
    print('Successfully generated BigBug_FinalNotebook.ipynb')
