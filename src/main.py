import os
import sys
import yaml
from pathlib import Path
from crewai import Agent, Task, Crew, Process
from tools.code_parser import read_target_file

class ROCmForgeEngine:
    def __init__(self):
        self.config_dir = Path(__file__).parent / 'config'
        self.agents_config = self._load_yaml(self.config_dir / 'agents.yaml')
        self.tasks_config = self._load_yaml(self.config_dir / 'tasks.yaml')
        
        # Enforce target fallback model parameters using standard litellm mapping 
        # Optimized for standard Open-Source platforms like Llama-3.2 running via AMD Open Ecosystem providers
        os.environ["OPENAI_API_BASE"] = os.getenv("AMD_CLOUD_API_BASE", "https://together.xyz")
        os.environ["OPENAI_API_KEY"] = os.getenv("AMD_CLOUD_API_KEY", "your-fallback-key")
        self.llm_model = "together_ai/meta-llama/Llama-3.2-3B-Instruct"

    def _load_yaml(self, path: Path) -> dict:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def initialize_orchestration(self, code_file_path: str) -> str:
        # Initialize Core Engineering Agents
        porter = Agent(
            config=self.agents_config['code_porting_agent'],
            tools=[read_target_file],
            llm=self.llm_model,
            verbose=True
        )
        
        analyst = Agent(
            config=self.agents_config['resource_monitoring_agent'],
            tools=[],
            llm=self.llm_model,
            verbose=True
        )

        # Initialize Core Pipeline Tasks
        task_one = Task(
            config=self.tasks_config['port_codebase_task'],
            agent=porter
        )
        
        task_two = Task(
            config=self.tasks_config['profile_resources_task'],
            agent=analyst
        )

        # Combine into sequential pipeline structure
        pipeline = Crew(
            agents=[porter, analyst],
            tasks=[task_one, task_two],
            process=Process.sequential,
            verbose=True
        )

        inputs = {"file_path": code_file_path}
        return pipeline.kickoff(inputs=inputs)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage error. Please pass target path: python main.py <target_code_file_path>")
        sys.exit(1)
        
    engine = ROCmForgeEngine()
    final_optimization_output = engine.initialize_orchestration(sys.argv[1])
    
    print("\n" + "="*40 + "\nROCMFORGE PIPELINE COMPLETE OUTPUT:\n" + "="*40)
    print(final_optimization_output)
  
