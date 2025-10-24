import simpy
import random
import statistics

 
# Simulation Parameters
RANDOM_SEED = 42
ARRIVAL_RATE = 30 / 60   # 30 calls per hour (calls/minute)
MEAN_SERVICE = 6         # average service time in minutes
SIM_TIME = 8 * 60        # total simulation time = 8 hours (in minutes)

# Call Process
def call_process(env, name, agents, wait_times, service_times):
    """Each incoming call is a process."""
    arrival_time = env.now

    with agents.request() as req:
        yield req  # wait until an agent is available
        wait = env.now - arrival_time
        wait_times.append(wait)

        # Service time
        service_time = random.expovariate(1 / MEAN_SERVICE)
        service_times.append(service_time)
        yield env.timeout(service_time)


# Call Generator
def call_generator(env, agents, wait_times, service_times):
    """Generate calls at random intervals."""
    call_id = 0
    while True:
        inter_arrival = random.expovariate(ARRIVAL_RATE)
        yield env.timeout(inter_arrival)
        call_id += 1
        env.process(call_process(env, f"Call-{call_id}", agents, wait_times, service_times))


# Main Simulation Function
def run_simulation(num_agents):
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    agents = simpy.Resource(env, capacity=num_agents)

    wait_times = []
    service_times = []

    env.process(call_generator(env, agents, wait_times, service_times))
    env.run(until=SIM_TIME)

    # Calculate metrics
    avg_wait = statistics.mean(wait_times) if wait_times else 0
    throughput = len(service_times) / SIM_TIME

    # Display results
    print("------------------------------------------------------")
    print(f"Results for {num_agents} Agents:")
    print(f"Average Wait (min): {avg_wait:.2f}")
    print(f"Throughput (calls/min): {throughput:.2f}")
    print("------------------------------------------------------")


# Run Simulation
if __name__ == "__main__":
    num_agents = 3  # set number of agents here
    run_simulation(num_agents)
