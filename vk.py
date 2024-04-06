import os

from forecast.engine import get_routes
from vk_api import VkGroupAdmin

if __name__ == '__main__':
    vk_manager = VkGroupAdmin(os.getenv('VK_TOKEN', 'token'), os.getenv('VK_API_VERSION', 'version'),
                              os.getenv('VK_GROUP_ID', 'group_id'))
    vk_post = get_routes()
