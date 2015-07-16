DEFAULT_PROFILE = 'profile-collective.awstats_hitcounter:default'

def upgrade_1100_to_1200(context):
    print "Upgrading to 0.0.1"
    context.runImportStepFromProfile(DEFAULT_PROFILE, 'portlets')
