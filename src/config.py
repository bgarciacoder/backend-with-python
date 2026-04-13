import settings

class Config:
    MONGO_URI = settings.MONGO_URI
    DEBUG = True
    JWT_SECRET_KEY = "3A3av5YZdbtdHRa7LAqPdkahwJMqxQVFM9D5dpMYywFUyRuXEGKkKpUTP0eEZlRv6DEvtI8elfdY6SBz9kmw2PIMks3f89Eq6BrI4CyESkVaZudwGcxu2zd8lgmE4De3b692kM9akUY6easThCGmmDm65arDoVKZScoAkEUoDPcBOptt1HWWUVg2pKcdWMoupatjjD8QzFMGHC06OqWYXTUh7yCSEdyxfLSRg8FRsOIcs2IrA9bgwM2PVQxSBy"
    API_KEY = settings.API_AUTH_TOKEN
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_COOKIE_HTTPONLY = True

# mongodb+srv://bgpastrana0901:SVpEwaYvgW0DBbpr@animeflask.a2hwdb7.mongodb.net/?retryWrites=true&w=majority&appName=animeflask