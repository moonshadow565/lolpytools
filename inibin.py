#!/usr/bin/env python
import struct
import io
import math
import json
import re

#Hashes string if two given hashesh "section*name" (asterix included)
def ihash(section, name = None):
    if not name == None:
        section = section + '*' + name
    ret = 0
    for c in section:
        ret = (ord(c.lower()) +((65599 * ret) & 0xffffffff)) & 0xffffffff
    return ret
    
# Note: rito likes to use ' and * prefixes to "comment out" stuff
all_inibin_fixlist = [
# LEVELS/MapX/DeathTimes.inibin
    [
        [ "DeathTimeScaling" ], [
            "IncrementTime",
            "PercentCap",
            "PercentIncrease",
            "StartTime",
        ]
    ],
    [
        [ "DeathTimeSettings" ], [
            "AllowDeathTimeMods",
            "StartDeathTimerForZombies",
        ]
    ],
    [
        [ "DeathWaveRespawn" ], [
            "WaveRespawnInterval",
        ]
    ],
    [
        [ "ExpGrantedOnDeath" ], [
            "BaseExpMultiple",
            "LevelDifferenceExpMultiple",
            "MinimumExpMultiple",
        ]
    ],
    [
        [ "TimeDeadPerLevel", "TimeDeadPerLevelTutorial" ],[
            *[ "Level{:02}".format(x) for x in range(0, 31) ]
        ]  
    ],
# LEVELS/MapX/ExpCurve.inibin
    [
        [ "EXP", "EXPTutorial" ], [
            *[ "Level{}".format(x) for x in range(0, 31) ]
        ]
    ],
# LEVELS/MapX/StatsProgression.inibin
    [
        [ "PerLevelStatsFactor" ], [
            *[ "Level{}".format(x) for x in range(0, 31) ]
        ]
    ],
# DATA/Globals/Critical.inibin
    [
        [ "Karma" ], [
            *[ "Critical{}".format(c) for c in range(0, 201) ]
        ]
    ],
# Data/Globals/Tips.inibin
# DATA/Globals/Bounty.inibin
    [
        [ "ARAM", "CLASSIC", "FIRSTBLOOD", "ODIN", "TUTORIAL", "Global" ], [
            "AssistDeathstreakReduction",
            "AssistDurationOverride",
            "AssistGoldPerStreak",
            "AssistGoldStreakCap",
            "AssistGoldStreakStart",
            "AssistPoolMax",
            "AssistPoolMaxValueTime",
            "AssistPoolMin",
            "AssistPoolMinValueTime",
            "AssistStreakBonus",
            "AssistStreakMin"
            "BaseGold",
            "BountyRoundDownIncrement",
            "DeathStreakPenalty",
            "DialogueClosedSound",
            "DialogueOpenedSound",
            "FirstBloodBonus",
            "GoldPoolForAssist",
            "KillStreakBonus",
            "MaxKillStreakBonus",
            "MaxViewable",
            "MinAssistsForStreak",
            "MinDeathsForStreak",
            "MinDeathStreakPenalty",
            "MinionGoldDeathstreakReductionRatio",
            "MinionGoldValueForBounty",
            "MinKillsForStreak",
            "MinMinionGoldValueForBounty",
            "PercentBountyResetOnDeath",
            "TimeBasedMinValuePercent",
            "TimeToMaxValueInSeconds",
            "TimeToMinValueInSeconds",
            "TipRecievedSound",
        ]
    ],
# DATA/Globals/Quests.inibin
    [
        [ "PrimaryQuests", "SecondaryQuests" ],[
            "CompletedText",
            "FailedText",
            "MaxViewable",
            "RecievedText",
            "TitleText",
        ]
    ],
    [
        [ "Coefficients" ],[
            "MCoefficient",
            "NCoefficient",
        ]
    ],
# spells, items, talents (everything is a buff -.-)
    [
        [ "BuffData" ], [
            "AlternateName",
            "ApplyMaterialOnHitSound",
            "DisplayName",
            "DynamicExtended",
            "DynamicTooltip",
            "DeathRecapPriority",
            *[ "Effect{}Level{}Amount".format(x, y) for x in range(0, 17) for y in range(0, 7) ],
            *[ "FloatStaticsDecimals{}".format(x) for x in range(0, 17) ],
            *[ "FloatVarsDecimals{}".format(x) for x in range(0, 17) ],
            "HideDurationInUI",
            "InventoryIcon",
            "ShowInTrackerUI",
            "Sound_VOEventCategory",
        ]
    ],
# DATA/Items/X.inibin
    [
        [ "Builds" ],[
            *[ "Item{}".format(x) for x in range(0, 17) ]
        ]
    ],
    [
        [ "Categories" ],[
            "Active",
            "Armor",
            "ArmorPenetration",
            "AttackSpeed",
            "Aura",
            "Boots",
            "Consumable",
            "CooldownReduction",
            "CriticalStrike",
            "Damage",
            "GoldPer",
            "Health",
            "HealthRegen",
            "Jungle",
            "LifeSteal",
            "MagicPenetration",
            "Mana",
            "ManaRegen",
            "Movement",
            "NonbootsMovement",
            "OnHit",
            "Slow",
            "SpellBlock",
            "SpellDamage",
            "SpellVamp",
            "Stealth",
            "Tenacity",
            "Trinket",
            "Vision",
        ]
    ],
    [
        [ "Data" ], [
            "AvatarUniqueEffect",
            "BuildDepth",
            "CanBeDropped",
            "CanBeSold",
            "ClearUndoHistoryOnActivate",
            "Clickable",
            "Consumed",
            "CooldownShowDisabledDuration",
            "Description",
            "DisappersOnDeath",
            "DisplayName",
            "DropsOnDeath",
            "DynamicTooltip",
            *[ "Effect{}Amount".format(x) for x in range(0, 16) ],
            "EffectRadius",
            "Epicness",
            "FlatArmorMod",
            "FlatArmorPenetrationMod",
            "FlatAttackRangeMod",
            "FlatAttackSpeedMod",
            "FlatBlockMod",
            "FlatBubbleRadius",
            "FlatCastRangeMod",
            "FlatCooldownMod",
            "FlatCritChanceMod",
            "FlatCritDamageMod",
            "FlatDodgeMod",
            "FlatEnergyPoolMod",
            "FlatEnergyRegenMod",
            "FlatEXPBonus",
            "FlatHPPoolMod",
            "FlatHPRegenMod",
            "FlatMagicDamageMod",
            "FlatMagicPenetrationMod",
            "FlatMagicPenetrationModPerLevel",
            "FlatMagicReduction",
            "FlatMissChanceMod",
            "FlatMovementSpeedMod",
            "FlatMPPoolMod",
            "FlatMPRegenMod",
            "FlatPhysicalDamageMod",
            "FlatPhysicalReduction",
            "FlatSpellBlockMod",
            "ForceLoad",
            "HideFromAll",
            "ImagePath",
            "InStore",
            "InventoryIcon",
            "InventorySlotMax",
            "InventorySlotMin",
            "IsRecipe",
            "ItemCalloutPlayer",
            "ItemCalloutSpectator",
            "ItemClass",
            "ItemGroup",
            "ItemId",
            "ItemType",
            "ItemVOGroup",
            "MaxGroupOwnable",
            "MaxStack",
            "PARStatName",
            "PercentArmorMod",
            "PercentArmorPenetrationMod",
            "PercentAttackRangeMod",
            "PercentAttackSpeedMod",
            "PercentBaseHPRegenMod",
            "PercentBaseMPRegenMod",
            "PercentBlockMod",
            "PercentBonusArmorPenetrationMod",
            "PercentBonusMagicPenetrationMod",
            "PercentBubbleRadius",
            "PercentCastRangeMod",
            "PercentCooldownMod",
            "PercentCritChanceMod",
            "PercentCritDamageMod",
            "PercentDodgeMod",
            "PercentEXPBonus",
            "PercentHealingAmountMod",
            "PercentHPPoolMod",
            "PercentHPRegenMod",
            "PercentLifeStealMod",
            "PercentMagicDamageMod",
            "PercentMagicPenetrationMod",
            "PercentMagicReduction",
            "PercentMovementSpeedMod",
            "PercentMPPoolMod",
            "PercentMPRegenMod",
            "PercentMultiplicativeAttackSpeedMod",
            "PercentMultiplicativeMovementSpeedMod",
            "PercentPhysicalDamageMod",
            "PercentPhysicalReduction",
            "PercentSlowResistMod",
            "PercentSpellBlockMod",
            "PercentSpellEffectivenessMod",
            "PercentSpellVampMod",
            "PercentTenacityCharacterMod",
            "PercentTenacityCleanseMod",
            "PercentTenacityItemMod",
            "PercentTenacityMasteryMod",
            "PercentTenacityRuneMod",
            "PlatformEnabled",
            "Price",
            *[ "RecipeItem{}".format(x) for x in range(0, 10) ],
            "RequiredChampion",
            *[ "RequiredItem{}".format(x) for x in range(0, 10) ],
            "RequiredLevel",
            "RequiredSpellName",
            "rFlatArmorModPerLevel",
            "rFlatArmorPenetrationMod",
            "rFlatArmorPenetrationModPerLevel",
            "rFlatCritChanceModPerLevel",
            "rFlatCritDamageModPerLevel",
            "rFlatDodgeMod",
            "rFlatDodgeModPerLevel",
            "rFlatEnergyModPerLevel",
            "rFlatEnergyRegenModPerLevel",
            "rFlatGoldPer10Mod",
            "rFlatHPModPerLevel",
            "rFlatHPRegenModPerLevel",
            "rFlatMagicDamageModPerLevel",
            "rFlatMagicPenetrationMod",
            "rFlatMagicPenetrationModPerLevel",
            "rFlatMovementSpeedModPerLevel",
            "rFlatMPModPerLevel",
            "rFlatMPRegenModPerLevel",
            "rFlatPhysicalDamageModPerLevel",
            "rFlatSpellBlockModPerLevel",
            "rFlatTimeDeadMod",
            "rFlatTimeDeadModPerLevel",
            "rPercentArmorPenetrationMod",
            "rPercentArmorPenetrationModPerLevel",
            "rPercentAttackSpeedModPerLevel",
            "rPercentCooldownMod",
            "rPercentCooldownModPerLevel",
            "rPercentMagicPenetrationMod",
            "rPercentMagicPenetrationModPerLevel",
            "rPercentMovementSpeedModPerLevel",
            "rPercentTimeDeadMod",
            "rPercentTimeDeadModPerLevel",
            "SellBackModifier",
            "ShowInActiveItemDisplay",
            "SpecialRecipe",
            "SpellName",
            "SpellLevel",
            "SpellCharges",
            "UsableInStore",
            "UseEffect",
            "UseWhenAcquired",
            *[ stat.format(par) for stat in [
                    "Flat{}PoolMod",
                    "Percent{}PoolMod",
                    "Flat{}RegenMod",
                    "Percent{}RegenMod",
                    "rFlat{}ModPerLevel",
                    "rFlat{}RegenModPerLevel",
                ] for par in [
                    "Mana",
                    "Energy",
                    "None",
                    "Shield",
                    "BattleFury",
                    "DragonFury",
                    "Rage",
                    "Heat",
                    "Ferocity",
                    "Bloodwell",
                    "Wind",
                    "Other",
                ]
            ],
        ]
    ],
# DATA/Spells/X.inibin, 
# DATA/Shared/Spells/X.inibin, 
# DATA/Characters/Y/Spells/X.inibin,
# DATa/Talents/X.inibin
    [
        [ "SpawningUI" ],
        [
            "BuffNameFilter",
            "MaxNumberOfUnits",
        ]
    ],
    [
        [ "SpellData" ],
        [
            "AfterEffectName",
            "AIBlockLevel",
            "AIEndOnly",
            "AILifetime",
            "AIRadius",
            "AIRange",
            "AISendEvent",
            "AISpeed",
            "AlternateName",
            "AlwaysSnapFacing",
            "AmmoCountHiddenInUI",
            "AmmoNotAffectedByCDR",
            "AmmoRechargeTime",
            *[ "AmmoRechargeTime{}".format(x) for x in range(0, 7) ],
            "AmmoUsed",
            *[ "AmmoUsed{}".format(x) for x in range(0, 7) ],
            "AnimationLeadOutName",
            "AnimationLoopName",
            "AnimationName",
            "AnimationWinddownName",
            "ApplyAttackDamage",
            "ApplyAttackEffect",
            "ApplyMaterialOnHitSound",
            "AttackDelayCastOffsetPercent",
            "BelongsToAvatar",
            "BounceRadius",
            "CanCastWhileDisabled",
            "CancelChargeOnRecastTime",
            "CanMoveWhileChanneling",
            "CannotBeSuppressed",
            "CanOnlyCastWhileDead",
            "CanOnlyCastWhileDisabled",
            "CantCancelWhileChanneling",
            "CantCancelWhileWindingUp",
            "CantCastWhileRooted",
            "CastConeAngle",
            "CastConeDistance",
            "CastFrame",
            "CastRadius",
            *[ "CastRadius{}".format(x) for x in range(0, 7) ],
            "CastRadiusSecondary",
            *[ "CastRadiusSecondary{}".format(x) for x in range(0, 7) ],
            "CastRadiusSecondaryTexture",
            "CastRadiusTexture",
            "CastRange",
            *[ "CastRange{}".format(x) for x in range(0, 7) ],
            "CastRangeDisplayOverride",
            *[ "CastRangeDisplayOverride{}".format(x) for x in range(0, 7) ],
            "CastRangeGrowthDuration",
            *[ "CastRangeGrowthDuration{}".format(x) for x in range(0, 7) ],
            "CastRangeGrowthMax",
            *[ "CastRangeGrowthMax{}".format(x) for x in range(0, 7) ],
            "CastRangeTextureOverrideName",
            "CastRangeUseBoundingBoxes",
            "CastTargetAdditionalUnitsRadius",
            "CastType",
            "ChannelDuration",
            *[ "ChannelDuration{}".format(x) for x in range(0, 7) ],
            "ChargeUpdateInterval",
            "CircleMissileAngularVelocity",
            "CircleMissileRadialVelocity",
            "ClientOnlyMissileTargetBoneName",
            "Coefficient",
            "Coefficient2",
            "ConsideredAsAutoAttack",
            "Cooldown",
            *[ "Cooldown{}".format(x) for x in range(0, 7) ],
            "CursorChangesInGrass",
            "CursorChangesInTerrain",
            "DeathRecapPriority",
            "DelayCastOffsetPercent",
            "DelayTotalTimePercent",
            "Description",
            "DisableCastBar",
            "DisplayName",
            "DoesntBreakChannels",
            "DoNotNeedToFaceTarget",
            "DrawSecondaryLineIndicator",
            "DynamicExtended",
            "DynamicTooltip",
            *[ "Effect{}Level{}Amount".format(x, y) for x in range(0, 17) for y in range(0, 7) ],
            "ExcludedUnitTags",
            "Flags",
            *[ "FloatStaticsDecimals{}".format(x) for x in range(0, 17) ],
            *[ "FloatVarsDecimals{}".format(x) for x in range(0, 17) ],
            "HaveAfterEffect",
            "HaveHitBone",
            "HaveHitEffect",
            "HavePointEffect",
            "HideRangeIndicatorWhenCasting",
            "HitBoneName",
            "HitEffectName",
            "HitEffectOrientType",
            "HitEffectPlayerName",
            "IgnoreAnimContinueUntilCastFrame",
            "IgnoreRangeCheck",
            "InventoryIcon",
            "InventoryIcon1",
            "InventoryIcon2",
            "InventoryIcon3",
            "IsDisabledWhileDead",
            "IsToggleSpell",
            "KeywordWhenAcquired",
            *[ "Level{}Desc".format(x) for x in range(0, 7) ],
            "LineDragLength",
            "LineMissileBounces",
            "LineMissileCollisionFromStartPoint",
            "LineMissileDelayDestroyAtEndSeconds",
            "LineMissileEndsAtTargetPoint",
            "LineMissileFollowsTerrainHeight",
            "LineMissileTargetHeightAugment",
            "LineMissileTimePulseBetweenCollisionSpellHits",
            "LineMissileTrackUnits",
            "LineMissileTrackUnitsAndContinues",
            "LineMissileUsesAccelerationForBounce",
            "LineTargetingBaseTextureOverrideName",
            "LineTargetingTargetTextureOverrideName",
            "LineWidth",
            *[ "LocationTargettingLength{}".format(x) for x in range(0, 8) ],
            *[ "LocationTargettingWidth{}".format(x) for x in range(0, 8) ],
            "LockConeToPlayer",
            "LookAtPolicy",
            "LuaOnMissileUpdateDistanceInterval",
            "ManaCost",
            *[ "ManaCost{}".format(x) for x in range(0, 8) ],
            *[ "Map{}_Effect{}Level{}Amount".format(m, x, y) for x in range(0, 17) for y in range(0, 7) for m in range(0,15) ],
            "MaxAmmo",
            *[ "MaxAmmo{}".format(x) for x in range(0, 7) ],
            "MaxGrowthRangeTextureName",
            "MaxGrowthLineBaseTextureName",
            "MaxGrowthLineTargetTextureName",
            "MaxHighlightTargets",
            "MinimapIcon",
            "MinimapIconDisplayFlag",
            "MinimapIconRotation",
            "MissileAccel",
            "MissileBoneName",
            "MissileBlockTriggersOnDestroy",
            "MissileEffect",
            "MissileEffectPlayer",
            "MissileFixedTravelTime",
            "MissileFollowsTerrainHeight",
            "MissileGravity",
            "MissileLifetime",
            "MissileMaxSpeed",
            "MissileMinSpeed",
            "MissileMinTravelTime",
            "MissilePerceptionBubbleRadius",
            "MissilePerceptionBubbleRevealsStealth",
            "MissileSpeed",
            "MissileTargetHeightAugment",
            "MissileUnblockable",
            "Name",
            "NoWinddownIfCancelled",
            "NumSpellTargeters",
            "OrientRadiusTextureFromPlayer",
            "OrientRangeIndicatorToCursor",
            "OrientRangeIndicatorToFacing",
            "OverrideCastTime",
            "ParticleStartOffset",
            "PhysicalDamageRatio",
            "PlatformEnabled",
            "PointEffectName",
            "Ranks",
            "RangeIndicatorTextureName",
            "RequiredUnitTags",
            "SelectionPreference",
            "Sound_CastName",
            "Sound_HitName",
            "Sound_VOEventCategory",
            "SpellCastTime",
            "SpellDamageRatio",
            "SpellRevealsChampion",
            "SpellTotalTime",
            "StartCooldown",
            "SubjectToGlobalCooldown",
            "TargeterConstrainedToRange",
            "TargettingType",
            "TextFlags",
            "TriggersGlobalCooldown",
            "UpdateRotationWhenCasting",
            "UseAnimatorFramerate",
            "UseAutoattackCastTime",
            "UseChargeChanneling",
            "UseChargeTargeting",
            "UseGlobalLineIndicator",
            "UseMinimapTargeting",
            "Version",
            "x1",
            "x2",
            "x3",
            "x4",
            "x5",
        ]
    ],
    [
        [ "OffsetTargeting" ],
        [
            "OT_ArcTextureOverride",
            "OT_ArcThicknessOffset",
            "OT_AreaRadius",
            "OT_AreaRadius1",
            "OT_AreaRadius2",
            "OT_AreaRadius3",
            "OT_AreaRadius4",
            "OT_AreaRadius5",
            "OT_AreaTextureOverride",
            "OT_DisplaysArcTargeter",
            "OT_DisplaysAreaIndicator",
            "OT_DisplaysLineIndicator",
            "OT_IsArcDirectionLeft",
            "OT_LineBaseTextureOverride",
            "OT_LineEndsAtTargetPoint",
            "OT_LineLength",
            "OT_LineLength1",
            "OT_LineLength2",
            "OT_LineLength3",
            "OT_LineLength4",
            "OT_LineLength5",
            "OT_LineNoIndicatorRadiusTextureOverride",
            "OT_LineTargetTextureOverride",
            "OT_LineWidth",
        ]
    ],
    [
        [ "SecondaryTargeting" ],
        [
            "CastRadius",
            "CastRadiusTexture",
            "CastRange",
            *[ "CastRange{}".format(x) for x in range(1, 8) ],
            "CastRangeGrowthMax",
            *[ "CastRangeGrowthMax{}".format(x) for x in range(1, 8) ],
            "CastRangeGrowthDuration",
            *[ "CastRangeGrowthDuration{}".format(x) for x in range(1, 8) ],
            "LineTargetingBaseTextureOverrideName",
            "LineTargetingTargetTextureOverrideName",
            "LineWidth",
            *[ "LocationTargettingWidth{}".format(x) for x in range(1, 7) ],
            *[ "LocationTargettingLength{}".format(x) for x in range(1, 7) ],
            "TargettingType",
        ]
    ],
    [
        [ *["SpellTargeter{}".format(x) for x in range(0, 9)] ],
        [
            *[ "{}{}".format(x,y) for x in [
                    "ConstraintPos",
                    "Center",
                    "End",
                    "Start",
                ] for y in [
                    "_AngleOffset",
                    "_BasePosition",
                    "_DistanceOffset",
                    "_OrientationType",
                ]
            ],
            "AlwaysDraw",
            "Center",
            "ConeAngle",
            "ConeRange",
            "ConeFollowsEnd",
            "ConstraintPos",
            "ConstraintRange",
            "DrawableType",
            "End",
            "FallbackDirection",
            "HasMaxGrowRangeTexture",
            "HideWithLineIndicator",
            "IsConstrainedToRange",
            "IsClockwiseArc",
            "Length",
            *[ "Length{}".format(x) for x in range(0,7) ],
            "LineStopsAtEndPosition",
            "LineTargetingTargetTextureOverrideName",
            "LineTargetingBaseTextureOverrideName",
            "LineWidth",
            "MaxAngle",
            "MaxAngleRangeFactor",
            "MinAngle",
            "MinAngleRangeFactor",
            "MinimumDisplayedRange",
            "OverrideBaseRange",
            *[ "OverrideBaseRange{}".format(x) for x in range(0,7) ],
            "OverrideRadius",
            *[ "OverrideRadius{}".format(x) for x in range(0,7) ],
            "RangeGrowthDuration",
            *[ "RangeGrowthDuration{}".format(x) for x in range(0,7) ],
            "RangeGrowthMax",
            *[ "RangeGrowthMax{}".format(x) for x in range(0,7) ],
            "RangeIndicatorTextureName",
            "Start",
            "TargettingType",
            "TextureBaseMaxGrow",
            "TextureBaseOverride",
            "TextureCone",
            "TextureConeMaxGrow",
            "TextureMaxGrow",
            "TextureOrientation",
            "TextureOverride",
            "TextureTargetMaxGrow",
            "TextureTargetOverride",
            "TextureWall",
            "Thickness",
            *[ "Thickness{}".format(x) for x in range(0,7) ],
            "ThicknessOffset",
            "UseCasterBoundingBox",
            "UseGlobalLineIndicator",
            "UseMinimapTargeting",
            "WallOrientation",
            "WallRotation",
        ]
    ],
# DATA/Characters/X/X.inibin
# DATA/Characters/Y/Skins/X/X.inibin
    [
        [ "ContextualAction" ], [
            "RuleConfigFile",
        ]
    ],
    [
        [ "Data" ],[
            "AbilityPowerIncPerLevel",
            "AcquisitionRange",
            "AllowPetControl",
            "AlwaysVisible",
            "Armor",
            "ArmorMaterial",
            "ArmorPerLevel",
            "AssetCategory",
            "AttackAutoInterruptPercent",
            "AttackCastTime",
            "AttackDelayCastOffsetPercent",
            "AttackDelayCastOffsetPercentAttackSpeedRatio",
            "AttackDelayOffsetPercent",
            "AttackRange",
            "AttackRank",
            "AttackSpeed",
            "AttackSpeedPerLevel",
            "AttackTotalTime",
            "BaseAbilityPower",
            "BaseCritChance",
            "BaseDamage",
            "BaseDodge",
            "BaseFactorHPRegen",
            "BaseFactorMPRegen",
            "BaseHP",
            "BaseMP",
            "BaseMissChance",
            "BaseSpellEffectiveness",
            "BaseStaticHPRegen",
            "BaseStaticMPRegen",
            "BotEnabled",
            "BotEnabledMM",
            "CastShadows",
            "ChampionId",
            "CharAudioNameOverride",
            "ChasingAttackRangePercent",
            "Classification",
            "CritDamageBonus",
            "CritPerLevel",
            "CS_easy",
            "CS_medium",
            "CS_hard",
            "DamagePerLevel",
            "DeathEventListeningRadius",
            "DeathTime",
            "DefenseRank",
            "DelayCastOffsetPercent",
            "DelayTotalTimePercent",
            "Description",
            "DifficultyRank",
            "DisableAggroIndicator",
            "DisableContinuousTargetFacing",
            "DisableGlobalDeathEffect",
            "DisableUltReadySounds",
            "DodgePerLevel",
            "DrawPARLikeHealth",
            "EnemyTooltip",
            "ExperienceRadius",
            "ExpGivenOnDeath",
            *[ v.format(a, x if x > 0 else  "") for a in [
                    "BaseAttack",
                    "BasicAttack",
                    "ExtraAttack",
                    "CritAttack",
                    "ExtraCritAttack",
                    "CriticalAttack",
                ] for v  in [
                    "{}{}",
                    "{}{}_AttackCastTime",
                    "{}{}_AttackCastDelayOffsetPercent",
                    "{}{}_AttackDelayCastOffsetPercent",
                    "{}{}_AttackDelayCastOffsetPercentAttackSpeedRatio",
                    "{}{}_AttackDelayOffsetPercent",
                    "{}{}_AttackTotalTime",
                    "{}{}_Probability",
                ] for x in range(0, 10)
            ],
            *[ "ExtraSpell{}".format(x) for x in range(0, 16) ],
            "FireworksEnabled",
            "FriendlyTooltip",
            "GameplayCollisionRadius",
            "GlobalExpGivenOnDeath",
            "GlobalGoldGivenOnDeath",
            "GoldGivenOnDeath",
            "GoldRadius",
            "HitFxScale",
            "HoverIndicatorRadius",
            "HoverIndicatorTextureName",
            "HoverLineIndicatorBaseTextureName",
            "HoverLineIndicatorTargetTextureName",
            "HoverLineIndicatorWidth",
            "HPPerLevel",
            "HPRegenPerLevel",
            "Immobile",
            "IsElite",
            "IsEpic",
            "IsImportantBotTarget",
            "IsMelee",
            "JointForAnimAdjustedSelection",
            "LevelDodge",
            "LevelSpellEffectiveness",
            "LocalExpGivenOnDeath",
            "LocalGoldGivenOnDeath",
            "LocalGoldSplitWithLastHitter",
            "Lore1",
            "Lore2",
            "MagicRank",
            "MaxLevels",
            "Metadata",
            "MonsterDataTableId",
            "MoveSpeed",
            "MPPerLevel",
            "MPRegenPerLevel",
            "Name",
            "NeverRender",
            "NoAutoAttack",
            "NoHealthBar",
            "OccludedUnitSelectableDistance",
            "OutlineBBoxExpansion",
            "PARColor",
            "PARDisplayThroughDeath",
            "PARFadeColor",
            "PARHasRegenText",
            "PARIncrements",
            "PARMaxSegments",
            "PARNameString",
            "PARType",
            *[ p.format(x) for x in range(1, 7) for p in [
                    "Passive{}",
                    "Passive{}Desc",
                    "PassLev{}Desc1",
                    "PassLev{}Desc2",
                    "PassLev{}Desc3",
                    "PassLev{}Desc4",
                    "PassLev{}Desc5",
                    "PassLev{}Desc6",
                    "Passive{}Icon",
                    "Passive{}Level1",
                    "Passive{}Level2",
                    "Passive{}Level3",
                    "Passive{}Level4",
                    "Passive{}Level5",
                    "Passive{}Level6",
                    "Passive{}Effect1",
                    "Passive{}Effect2",
                    "Passive{}Effect3",
                    "Passive{}Effect4",
                    "Passive{}Effect5",
                    "Passive{}Effect6",
                    "Passive{}LuaName",
                    "Passive{}Name",
                    "Passive{}NumEffects",
                    "Passive{}Range",
                ]
            ],
            "PassiveSpell",
            "PathfindingCollisionRadius",
            "PerceptionBubbleRadius",
            "PlatformEnabled",
            "PostAttackMoveDelay",
            "RecordAsWard",
            "Roles",
            "SearchTags",
            "SelectionHeight",
            "SelectionRadius",
            "SequentialAutoAttacks",
            "ServerOnly",
            "ShouldFaceTarget",
            "Significance",
            "SkipDrawOutline",
            "SoulGivenOnDeath",
            *[ s.format(x) for x in range(1, 5) for s in [
                    "Spell{}",
                    "Spell{}Desc",
                    "Spell{}DisplayName",
                    "SpellsUpLevels{}",
                ]
            ],
            "SpellBlock",
            "SpellBlockPerLevel",
            "SR_easy",
            "SR_medium",
            "SR_hard",
            "Tips1",
            "Tips2",
            "Tips3",
            "TowerTargetingPriorityBoost",
            "TriggersOrderAcknowledgementVO",
            "UnitTags",
            "UseChampionVisibility",
            "UseRingIconForKillCallout",
            "WeaponMaterial",
            "`WeaponMaterial",
            "WeaponMaterial1",
            "WeaponMaterial2",
            "WeaponMaterial3",
            "WeaponMaterial4",
        ]
    ],
    [
        [ "DefaultAnimations" ],[
            *[ "Animation{}".format(x) for x in range(1, 10) ],
            "NumberOfAnimations",
            "Significance",
        ]
    ],
    [
        [ "Evolution" ],[
            "EnabledWhileDead",
            "EvolveTitle",
            "Spell1EvolveDesc",
            "Spell1EvolveIcon",
            "Spell2EvolveDesc",
            "Spell2EvolveIcon",
            "Spell3EvolveDesc",
            "Spell3EvolveIcon",
            "Spell4EvolveDesc",
            "Spell4EvolveIcon",
        ]
    ],
    [
        [ "HealthBar" ], [
            "AttachToBone",
            "HPPerTick",
            "ParallaxOffset",
            "Scale",
            "ShowWhileUntargetable",
            "UnitBarKey",
            "WorldOffset",
            "XOffset",
            "YOffset",
        ]
    ],
    [
        [ "IdleParticles" ],[
            "BeamParticle",
            "BeamShouldAlwayStargetEnemy",
            "BeamTargetParticle",
            "ChampTargetingParticle",
            "GameplayCollisionRadius",
            "NumberOfParticles",
            "SelfIllumination",
            *[ "Particle{}".format(x) for x in range(0, 100) ],
            "TowerTargetingParticle",
            "TowerTargetingParticle2",
            "TowerTargetingParticle2Death",
        ]
    ],
    [
        [ *[ "Info{}".format(x if x > 0 else "") for x in range(0, 8) ] ], [
            "IconCircle",
            "IconCircleScale",
            "IconMinimap",
            "IconSquare",
        ]
    ],
    [
        [ "Interaction" ], [
            "DoubleSided",
            "IdleAnim",
            "RandomizeIdleAnimPhase",
        ]
    ],
    [
        [ *[ "MeshSkin{}".format(x if x > 0 else "") for x in range(0, 30) ] ], [
            "Animations",
            "ArmorMaterial",
            "AttributeFlags",
            "Body",
            "BrushAlphaOverride",
            "CastShadows",
            "ChampionSkinID",
            "ChampionSkinName",
            "DisablePreload",
            "EmissiveTexture",
            "ExtraCharacterPreloads",
            "Fresnel",
            "FresnelBlue",
            "FresnelGreen",
            "FresnelRed",
            "GlossTexture",
            "GlowFactor",
            "HPPerTick",
            "IconAvatar",
            "IsOpaque",
            *[ mat.format(x) for x in range(0,5) for mat in [
                    "MaterialOverride{}BlendMode",
                    "MaterialOverride{}GlossTexture",
                    "MaterialOverride{}EmissiveTexture",
                    "MaterialOverride{}FixedAlphaScrolling",
                    "MaterialOverride{}Priority",
                    "MaterialOverride{}RenderingMode",
                    "MaterialOverride{}SubMesh",
                    "MaterialOverride{}Texture",
                    "MaterialOverride{}UVScroll",
                ]
            ],
            "MaterialOverrideTransMap",
            "MaterialOverrideTransSource",
            "MaterialOverridePriority",
            "OverrideBoundingBox",
            "ParallaxOffset",
            "ParticleOverride_ChampionKillDeathParticle",
            "ParticleOverride_DeathParticle",
            "ReflectionFresnel",
            "ReflectionFresnelBlue",
            "ReflectionFresnelGreen",
            "ReflectionFresnelRed",
            "ReflectionMap",
            "ReflectionOpacityDirect",
            "ReflectionOpacityGlancing",
            "Scale",
            "SelfIllumination",
            "SimpleSkin",
            "Skeleton",
            "SkinScale",
            "SkinAudioNameOverride",
            "SkipVOOverride",
            "SubmeshesToHide",
            "Texture",
            "TextureLow",
            "UsesSkinVO",
            "UnitBarKey",
            "VOOverride",
            "Weight",
            "WorldOffset",
            "XOffset",
            "YOffset",
        ]
    ],
    [
        [ "Minimap" ],[
            "MinimapIconOverride",
        ]
    ],
    [
        [ "Minion" ],[
            "AlwaysUpdatePAR",
            "AlwaysVisible",
            "IsTower",
        ]
    ],
    [
        [ "Package" ],[
            "FallbackPackage",
            "FallbackINI",
        ]
    ],
    [
        [ "RecItems", "TutorialRecItems" ], [
            *[ "RecItem{}".format(x) for x in range(1, 7) ]
        ]
    ],
    [
        [ "Sounds" ], [
            "Attack1",
            "Attack2",
            "Attack3",
            "Attack4",
            "Click1",
            "Click2",
            "Click3",
            "Click4",
            "Death",
            "Move1",
            "Move2",
            "Move3",
            "Move4",
            "Ready",
            "Special1",
            "Special2",
        ]
    ],
    [
        [ "Useable" ],[
            "AllyCanUse",
            "CooldownSpellSlot",
            "EnemyCanUse",
            "GoldRedirectTargetUseableOnly",
            "HeroUseSpell",
            "IsUseable",
            "MinionUseable",
            "MinionUseSpell",
        ]
    ]
]

def add2fixdict(section, name, result = None):
    if result == None:
        result = {}
    h = str(ihash(section, name))
    if h in result:
        old = result[h]
        if old[0].lower() != section.lower() or old[1].lower() != name.lower():
            print("Collision", section, name, "=", h, "with", old[0], old[1])
    else:
        result[h] = [section, name]
    return result
    
# converts map to fix dictionary
def map2fixdict(m, result = None):
    if result == None:
        result = {}
    for section in m:
        for name in m[section]:
            add2fixdict(section, name, result)
    return result

def fixdict2map(fd, result = None):
    if result == None:
        result = {}
    for h in fd:
        section = fd[h][0]
        name = fd[h][1]
        if not section in result:
            result[section] = {}
        result[section][name] = h
    return result

# converts fix list to fix dict
def fixlist2fixdict(arr, result = None):
    if result == None:
        result = {}
    for sn in arr:
        for section in sn[0]:
            for name in sn[1]:
                add2fixdict(section, "'"+name, result)
                add2fixdict(section, name, result)
    return result
all_inibin_fixdict = fixlist2fixdict(all_inibin_fixlist)


# WARNING: keep inibin and troybin separate because they like to conflict
# unhashes .inibin with dictionary
def fix_inibin(inib, fixd = None):
    if fixd == None:
        fixd = all_inibin_fixdict
    if not "Values" in inib:
        inib["Values"] = {}
    if not "UNKNOWN_HASHES" in inib:
        inib["UNKNOWN_HASHES"] = {}
    unk = inib["UNKNOWN_HASHES"]
    values = inib["Values"]
    for h in unk.copy():
        if h in fixd:
            section = fixd[h][0]
            name = fixd[h][1]
            if not section in values:
                values[section] = {}
            values[section][name] = unk[h]
            del unk[h]

# Sanitize regexp's
RE_TRUE = re.compile(r"^\s*true\s*$", re.IGNORECASE);
RE_FALSE = re.compile(r"^\s*false\s*$", re.IGNORECASE);
RE_NAN = re.compile(r"^/s*NaN/s*$", re.IGNORECASE);
NAN_VALUE = float('nan')
RE_INT = re.compile(r"^\s*[-+]?\d+\s*$", re.IGNORECASE);
RE_DECIMAL = re.compile(r"^\s*[+-]?(?:\d+\.\d*|\d*\.\d+|\d+)(?:e[+-]?\d+)?\s*$", re.IGNORECASE);
RE_INT_VEC = re.compile(r"^\s*(?:[-+]?\d+\s+)+(?:[-+]?\d+)\s*$", re.IGNORECASE);
RE_DECIMAL_VEC = re.compile(r"^\s*(?:[+-]?(?:\d+\.\d*|\d*\.\d+|\d+)(?:e[+-]?\d+)?\s+)+([+-]?(?:\d+\.\d*|\d*\.\d+|\d+)(?:e[+-]?\d+)?)\s*$", re.IGNORECASE);

# converts values stored in string to their right value types
def sanitize_str(data):
    if RE_TRUE.match(data):
        return 1
    elif RE_FALSE.match(data):
        return 0
    elif RE_NAN.match(data):
        return NAN_VALUE
    elif RE_INT_VEC.match(data):
        return [int(x) for x in data.replace('\t', ' ').split(' ') if x]
    elif RE_DECIMAL_VEC.match(data):
        return [float(x) for x in data.replace('\t', ' ').split(' ') if x]
    elif RE_INT.match(data):
        return int(data)
    elif RE_DECIMAL.match(data):
        return float(data)
    else:
        return data
    
#Reads inibin from binary buffer to dictionary(keys and values in strings)
#Copies results to target and returns (optional argument)
def read_2(buffer, target):
    def read_flags(buffer, count):
        result = []
        bools = buffer.read(math.ceil(count/8))
        for index in range(0, count):
            result.append(bool((bools[index // 8] >> (index%8))  & 1))
        return result

    def read_numbers(buffer, fmt, count = 1, mul = 1):
        result = {}
        num = struct.unpack("<H", buffer.read(2))[0]
        keys = []
        for x in range(0, num):
            keys.append(struct.unpack("<I", buffer.read(4))[0])
        for x in range(0, num):
            tmp = []
            for y in range(0, count):
                tmp.append(struct.unpack(fmt, buffer.read(struct.calcsize(fmt)))[0] * mul)
            result[keys[x]] = tmp[0] if count == 1 else tmp
        return result

    def read_bools(buffer):
        result = {}
        num = struct.unpack("<H", buffer.read(2))[0]
        keys = []
        for x in range(0, num):
            keys.append(struct.unpack("<I", buffer.read(4))[0])
        bools = read_flags(buffer, num)
        for x in range(0, num):
            result[keys[x]] = int(bools[x])         
        return result

    def read_strings(buffer, stringsLength):
        result = {}
        offsets = read_numbers(buffer, "<H")
        data = buffer.read(stringsLength)
        for key in offsets:
            o = int(offsets[key])
            t = ""
            while data[o] != 0:
                t = t + chr(data[o])
                o = o + 1
            result[key] = sanitize_str(t)
        return result
    stringsLength = struct.unpack("<H", buffer.read(2))[0]
    flags = read_flags(buffer, 16)
    read_conf = [
        [read_numbers, ["<i"]],           #0  - 1 x int
        [read_numbers, ["<f"]],           #1  - 1 x float 
        [read_numbers, ["<B", 1, 0.1]],   #2  - 1 x byte * 0.1
        [read_numbers, ["<h"]],           #3  - 1 x short
        [read_numbers, ["<B"]],           #4  - 1 x byte 
        [read_bools, []],                 #5  - 1 x bools 
        [read_numbers, ["<B", 3, 0.1]],   #6  - 3 x byte * 0.1
        [read_numbers, ["<f", 3]],        #7  - 3 x float
        [read_numbers, ["<B", 2, 0.1]],   #8  - 2 x byte * 0.1
        [read_numbers, ["<f", 2]],        #9  - 2 x float
        [read_numbers, ["<B", 4, 0.1]],   #10 - 4 x byte * 0.1
        [read_numbers, ["<f", 4]],        #11 - 4 x float
        [read_strings, [stringsLength]],  #12 - strings
        # TODO: are strings stored at the end of file allways??
        #[read_numbers, ["<q"]],           #13 - long long
    ]
    for x in range(0, 16):
        if flags[x]:
            if x < len(read_conf):
                target.update(read_conf[x][0](buffer, *(read_conf[x][1])))
            else:
                raise "Unknown inibin flag {} in {}!".format(x, buffer.name)
    return target

# reads version 1 .inibin
def read_1(buffer, target):
    buffer.read(3)
    entryCount = struct.unpack("I", buffer.read(4))[0]
    dataCount = struct.unpack("I", buffer.read(4))[0]
    offsets = {}
    for i in range(0, entryCount):
        h = struct.unpack("I", buffer.read(4))[0]
        o = struct.unpack("I", buffer.read(4))[0]
        offsets[h] = o
    data = buffer.read(dataCount)
    result = {}
    for key in offsets:
        o = int(offsets[key])
        t = ""
        while data[o] != 0:
            t = t + chr(data[o])
            o = o + 1
        result[key] = sanitize_str(t)
    target.update(result)
    return target

# reads .inibin from bianry buffer with auto-detecting version
def read(buffer, result = None):
    if result == None:
        result = {
            "Values": {},
            "UNKNOWN_HASHES": {}
        }
    else:
        if not "Values" in result:
            result["Values"] = {}
        if not "UNKNOWN_HASHES" in result:
            result["UNKNOWN_HASHES"] = {}
    target = result["UNKNOWN_HASHES"]
    version = struct.unpack("B", buffer.read(1))[0]
    if version == 2:
        read_2(buffer, target)
    elif version == 1:
        read_1(buffer, target)
    else:
        raise "Unknow version!"
    return result
    
# reads .inibin from binary file on filesystem
def from_file(name, result = None):
    return read(open(name, "rb"), result)

# gets entry in .ini/.inibin
def get(target, section, name, default = None):
    if section in target["Values"] and name in target["Values"][section]:
        return target["Values"][section][name]
    else:
        h = ihash(section, name)
        return target["UNKNOWN_HASHES"][h] if h in target["UNKNOWN_HASHES"] else default

def load_json(name):
    with open(name, 'r') as inf:
        return json.load(inf)
def save_json(name, j):
    with open(name, 'w') as outf:
        outf.write(json.dumps(j, indent=2, sort_keys=True))
def to_json(target):
    return json.dumps(target, indent=2)
