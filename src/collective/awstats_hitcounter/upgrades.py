DEFAULT_PROFILE = 'profile-collective.awstats_hitcounter:default'

def upgrade_1100_to_1200(context):
    print "Upgrading to 0.1.5"
    context.runImportStepFromProfile(DEFAULT_PROFILE, 'portlets')
    context.runImportStepFromProfile(DEFAULT_PROFILE, 'cssregistry')
    context.runImportStepFromProfile(DEFAULT_PROFILE, 'portal_registry')
