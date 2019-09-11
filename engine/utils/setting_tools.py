import logging

from engine.algorithms.DDPG.ddpg import DDPG
from engine.algorithms.DDPG_PARAMNOISE.ddpg_param_noise import DDPG_Param_Noise
from engine.algorithms.DDPG_POLYRL.ddpg import DDPGPolyRL

logger = logging.getLogger(__name__)


def get_agent_type(state_dim, action_dim, max_action, args, env,memory,device):
    agent = None
    # Adds noise to the selected action by the policy"
    if (args.algo == "DDPG"):
        agent = DDPG(state_dim, action_dim, max_action, expl_noise=args.expl_noise,
                     action_high=env.action_space.high, action_low=env.action_space.low, tau=args.tau,
                     device=device)
    elif (args.algo == "DDPG_PARAM"):
        agent = DDPG_Param_Noise(state_dim, action_dim, max_action, expl_noise=args.expl_noise,
                     action_high=env.action_space.high, action_low=env.action_space.low, tau=args.tau,
                     initial_stdev=args.initial_stdev, noise_scale=args.noise_scale,memory=memory,
                                 device=device)
    elif (args.algo == "DDPG_POLYRL"):
        agent = DDPGPolyRL(state_dim, action_dim, max_action, expl_noise=args.expl_noise,
                     action_high=env.action_space.high, action_low=env.action_space.low, tau=args.tau,
                     device=device, gamma=args.gamma, betta=args.betta, epsilon=args.epsilon,
                     sigma_squared=args.sigma_squared,lambda_=args.lambda_,nb_actions=env.action_space.shape[0],
                     nb_observations=env.observation_space.shape[0],min_action=float(min(env.action_space.low)))
    #     poly_rl_alg = PolyRL(gamma=args.gamma, betta=args.betta, epsilon=args.epsilon, sigma_squared=args.sigma_squared,
    #                          actor_target_function=agent.select_action_from_target_actor, env=env, lambda_=args.lambda_)
    #     agent.set_poly_rl_alg(poly_rl_alg)
    # elif (args.algo == "DIV_DDPG"):
    #     agent = DivDDPGActor(gamma=args.gamma, tau=args.tau, hidden_size=args.hidden_size, ounoise=ounoise,
    #                          num_inputs=env.observation_space.shape[0], action_space=env.action_space,
    #                          lr_actor=args.lr_actor, lr_critic=args.lr_critic, phi=args.phi, linear_flag=args.linear_diverse_noise)
    else:
        logger.info("Algorithm {} has not yet implemented! please select among 'DDPG, PARAM_DDPG, POLYRL_DDPG, DIV_DDPG'".format(args.algo))
        raise NotImplementedError
    logger.info("Algorithm {} has been initialized".format(args.algo))
    return agent
