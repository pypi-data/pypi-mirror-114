#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <stdio.h>
#include <vector>
#include <string>
using namespace std;
#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

class AssetStats
{
public:
	int name;
	int minCost;
	int gasCost;
	int supCost;
	int supProvide;
	int duration;
	int parent;
	vector<int > techReqs;
	int maxQuantity;
	bool canChrono;
	AssetStats(int myname, int myminCost, int mygasCost, int mysupCost, int mysupProvide, int myduration, int myparent, vector<int > mytechReqs, int mymaxQuantity, bool mycanChrono) {
		name = myname;
		minCost = myminCost;
		gasCost = mygasCost;
		supCost = mysupCost;
		supProvide = mysupProvide;
		duration = myduration;
		parent = myparent;
		techReqs = mytechReqs;
		maxQuantity = mymaxQuantity;
		canChrono = mycanChrono;
	}
};

class Entity
{
public:
	int assetType;
	double timeToComplete;
	double timeQueueFree;
	double timeChronoLeft;
	double energy;
	int executor;
	int child;
	bool isComplete;
	Entity(int myAssetType, double myTimeToComplete, double myTimeQueueFree, double myTimeChronoLeft, double myEnergy, int myExecutor, int myChild, bool myIsComplete) {
		assetType = myAssetType;
		timeToComplete = myTimeToComplete;
		timeQueueFree = myTimeQueueFree;
		timeChronoLeft = myTimeChronoLeft;
		energy = myEnergy;
		executor = myExecutor;
		child = myChild;
		isComplete = myIsComplete;
	}
	Entity(const Entity& origEntity) {
		assetType = origEntity.assetType;
		timeToComplete = origEntity.timeToComplete;
		timeQueueFree = origEntity.timeQueueFree;
		timeChronoLeft = origEntity.timeChronoLeft;
		energy = origEntity.energy;
		executor = origEntity.executor;
		child = origEntity.child;
		isComplete = origEntity.isComplete;
	}
};

class Names
{
public:
	int dummy;
	int probe;
	int zealot;
	int sentry;
	int stalker;
	int adept;
	int hightemplar;
	int darktemplar;
	int observer;
	int warpprism;
	int immortal;
	int colossus;
	int disruptor;
	int phoenix;
	int voidray;
	int oracle;
	int tempest;
	int carrier;
	int warpzealot;
	int warpsentry;
	int warpstalker;
	int warpadept;
	int warphightemplar;
	int warpdarktemplar;

	int nexus;
	int pylon;
	int assimilator;
	int gateway;
	int forge;
	int photoncannon;
	int shieldbattery;
	int warpgate;
	int cyberneticscore;
	int twilightcouncil;
	int roboticsfacility;
	int stargate;
	int templararchives;
	int darkshrine;
	int roboticsbay;
	int fleetbeacon;

	int groundweapons1;
	int groundarmor1;
	int airweapons1;
	int airarmor1;
	int shields1;
	int groundweapons2;
	int groundarmor2;
	int airweapons2;
	int airarmor2;
	int shields2;
	int groundweapons3;
	int groundarmor3;
	int airweapons3;
	int airarmor3;
	int shields3;
	int charge;
	int graviticdrive;
	int resonatingglaives;
	int graviticboosters;
	int fluxvanes;
	int anionpulsecrystals;
	int extendedthermallance;
	int psionicstorm;
	int blink;
	int shadowstride;
	int warpgateresearch;
	int gravitoncatapult;

	int chronoboost;

	Names() {
		dummy = 0;
		probe = 1;
		zealot = 2;
		sentry = 3;
		stalker = 4;
		adept = 5;
		hightemplar = 6;
		darktemplar = 7;
		observer = 8;
		warpprism = 9;
		immortal = 10;
		colossus = 11;
		disruptor = 12;
		phoenix = 13;
		oracle = 14;
		voidray = 15;
		tempest = 16;
		carrier = 17;
		warpzealot = 18;
		warpsentry = 19;
		warpstalker = 20;
		warpadept = 21;
		warphightemplar = 22;
		warpdarktemplar = 23;

		nexus = 24;
		pylon = 25;
		assimilator = 26;
		gateway = 27;
		forge = 28;
		photoncannon = 29;
		shieldbattery = 30;
		warpgate = 31;
		cyberneticscore = 32;
		twilightcouncil = 33;
		roboticsfacility = 34;
		stargate = 35;
		templararchives = 36;
		darkshrine = 37;
		roboticsbay = 38;
		fleetbeacon = 39;

		groundweapons1 = 40;
		groundarmor1 = 41;
		airweapons1 = 42;
		airarmor1 = 43;
		shields1 = 44;
		groundweapons2 = 45;
		groundarmor2 = 46;
		airweapons2 = 47;
		airarmor2 = 48;
		shields2 = 49;
		groundweapons3 = 50;
		groundarmor3 = 51;
		airweapons3 = 52;
		airarmor3 = 53;
		shields3 = 54;
		charge = 55;
		graviticdrive = 56;
		resonatingglaives = 57;
		graviticboosters = 58;
		fluxvanes = 59;
		anionpulsecrystals = 60;
		extendedthermallance = 61;
		psionicstorm = 62;
		blink = 63;
		shadowstride = 64;
		warpgateresearch = 65;
		gravitoncatapult = 66;

		chronoboost = 67;
	}
};

class ProtossMacroEnv
{
public:
	double minerals;
	double gas;
	int mProbeCount;
	int gProbeCount;
	int maxSupply;
	int maxFutureSupply;
	int supply;
	double time;
	vector<Entity> entityList;
	vector<int> goalState;
	vector<int> state;
	bool done;

	static double REGEN_RATE;
	static int ACTION_SPACE;
	static vector<AssetStats> assetList;
	static Names n;

	ProtossMacroEnv() {
		REGEN_RATE = 1;
		ACTION_SPACE = 68;
		loadStatCatalog();
		for (int i = 0; i < assetList.size(); i++) {
			state.push_back(0);
		}
		initEntityList();
		initGlobalState();
		initGoalState();
	}

	ProtossMacroEnv(const ProtossMacroEnv& env) {
		//copy raw 
		minerals = env.minerals;
		gas = env.gas;
		mProbeCount = env.mProbeCount;
		gProbeCount = env.gProbeCount;
		maxSupply = env.maxSupply;
		maxFutureSupply = env.maxFutureSupply;
		supply = env.supply;
		time = env.time;
		REGEN_RATE = env.REGEN_RATE;

		//reload these from scratch for now
		loadStatCatalog();

		//deep copy
		copyEntityList(env.entityList);
		for (int i : env.state) {
			state.push_back(i);
		}
	}

	void loadStatCatalog() {
		if (assetList.size() > 0)return;
		assetList = {
			//placeholder
			AssetStats(n.dummy, 0, 0, 0, 0, 0, n.dummy, { n.dummy }, 1, false),
			//units
			AssetStats(n.probe, 50, 0, 1, 0, 12, n.nexus, { n.nexus }, 20, false),
			AssetStats(n.zealot, 100,0,2,0,27,n.gateway,{n.gateway}, 10, false),
			AssetStats(n.sentry,50,100,2,0,26,n.gateway,{n.gateway,n.cyberneticscore},100,false),
			AssetStats(n.stalker,215,50,2,0,30,n.gateway,{n.gateway,n.cyberneticscore},10,false),
			AssetStats(n.adept,100,25,2,0,27,n.gateway,{n.gateway,n.cyberneticscore},10,false),
			AssetStats(n.hightemplar,50,150,2,0,39,n.gateway,{n.gateway,n.templararchives},10,false),
			AssetStats(n.darktemplar,125,125,2,0,39,n.gateway,{n.gateway,n.darkshrine},10,false),
			AssetStats(n.observer,25,75,1,0,21,n.roboticsfacility,{n.roboticsfacility},10,false),
			AssetStats(n.warpprism,200,0,2,0,36,n.roboticsfacility,{n.roboticsfacility},10,false),
			AssetStats(n.immortal,275,100,4,0,39,n.roboticsfacility,{n.roboticsfacility},10,false),
			AssetStats(n.colossus,300,200,6,0,54,n.roboticsfacility,{n.roboticsfacility,n.roboticsbay},10,false),
			AssetStats(n.disruptor,150,150,3,0,36,n.roboticsfacility,{n.roboticsfacility,n.roboticsbay},10,false),
			AssetStats(n.phoenix,150,100,2,0,25,n.stargate,{n.stargate},10,false),
			AssetStats(n.oracle,150,150,3,0,37,n.stargate,{n.stargate},10,false),
			AssetStats(n.voidray,200,100,4,0,37,n.stargate,{n.stargate},10,false),
			AssetStats(n.tempest,250,175,5,0,43,n.stargate,{n.stargate,n.fleetbeacon},10,false),
			AssetStats(n.carrier,350,250,6,0,64,n.stargate,{n.stargate,n.fleetbeacon},10,false),
			AssetStats(n.warpzealot, 100,0,2,0,7,n.warpgate,{n.warpgate}, 10, false),
			AssetStats(n.warpsentry,50,100,2,0,7,n.warpgate,{n.warpgate,n.cyberneticscore},100,false),
			AssetStats(n.warpstalker,215,50,2,0,7,n.warpgate,{n.warpgate,n.cyberneticscore},10,false),
			AssetStats(n.warpadept,100,25,2,0,7,n.warpgate,{n.warpgate,n.cyberneticscore},10,false),
			AssetStats(n.warphightemplar,50,150,2,0,7,n.warpgate,{n.warpgate,n.templararchives},10,false),
			AssetStats(n.warpdarktemplar,125,125,2,0,7,n.warpgate,{n.warpgate,n.darkshrine},10,false),
			//buildings
			AssetStats(n.nexus, 400, 0, 0,15, 71, NULL,{}, 3, true),
			AssetStats(n.pylon, 100, 0, 0,8, 18, NULL,{}, 10, false),
			AssetStats(n.assimilator, 75, 0, 0,0, 21, NULL,{}, 8, false),
			AssetStats(n.gateway, 150, 0, 0,0, 46, NULL,{n.pylon}, 10, true),
			AssetStats(n.forge, 150, 0, 0,0, 32, NULL,{n.pylon}, 3, true),
			AssetStats(n.photoncannon, 150, 0, 0,0, 29, NULL,{n.forge}, 5, false),
			AssetStats(n.shieldbattery, 100, 0, 0,0, 29, NULL,{n.cyberneticscore}, 5, false),
			AssetStats(n.warpgate, 0, 0, 0,0, 7, NULL,{n.warpgateresearch,n.gateway}, 10, true),
			AssetStats(n.cyberneticscore, 150, 0, 0, 0,36, NULL,{n.gateway}, 3, true),
			AssetStats(n.twilightcouncil, 150, 100, 0,0, 36, NULL,{n.cyberneticscore}, 3, true),
			AssetStats(n.roboticsfacility, 150, 100, 0, 0,46, NULL,{n.cyberneticscore}, 10, true),
			AssetStats(n.stargate, 150, 150, 0, 0,43, NULL,{n.cyberneticscore}, 10, true),
			AssetStats(n.templararchives, 150, 200, 0,0, 36, NULL,{n.twilightcouncil}, 1, true),
			AssetStats(n.darkshrine, 150, 150, 0,0, 71, NULL,{n.twilightcouncil}, 1, true),
			AssetStats(n.roboticsbay, 150, 150, 0,0, 46, NULL,{n.roboticsfacility}, 3, true),
			AssetStats(n.fleetbeacon, 300, 200, 0,0, 43, NULL,{n.stargate}, 3, true),
			//upgrades
			AssetStats(n.groundweapons1, 100, 100, 0,0, 129,n.forge,{n.forge}, 1, false),
			AssetStats(n.groundarmor1, 100, 100, 0,0, 129,n.forge,{n.forge}, 1, false),
			AssetStats(n.airweapons1, 100, 100, 0,0, 129,n.cyberneticscore,{n.cyberneticscore}, 1, false),
			AssetStats(n.airarmor1, 150, 150, 0,0, 129,n.cyberneticscore,{n.cyberneticscore}, 1, false),
			AssetStats(n.shields1, 150, 150, 0,0, 129, n.forge,{n.forge}, 1, false),
			AssetStats(n.groundweapons2, 150, 150, 0,0, 154,n.forge,{n.twilightcouncil, n.forge, n.groundweapons1}, 1, false),
			AssetStats(n.groundarmor2, 150, 150, 0,0, 154,n.forge,{n.twilightcouncil, n.forge, n.groundarmor1}, 1, false),
			AssetStats(n.airweapons2, 175, 175, 0,0, 154,n.cyberneticscore,{n.cyberneticscore, n.fleetbeacon, n.airweapons1}, 1, false),
			AssetStats(n.airarmor2, 225, 225, 0,0, 154,n.cyberneticscore,{n.cyberneticscore, n.fleetbeacon, n.airarmor1}, 1, false),
			AssetStats(n.shields2, 225, 225, 0,0, 154, n.forge,{n.twilightcouncil, n.forge, n.shields1}, 1, false),
			AssetStats(n.groundweapons3, 200, 200, 0,0, 179,n.forge,{n.twilightcouncil, n.forge, n.groundweapons2}, 1, false),
			AssetStats(n.groundarmor3, 200, 200, 0,0, 179,n.forge,{n.twilightcouncil, n.forge, n.groundarmor2}, 1, false),
			AssetStats(n.airweapons3, 250, 250, 0,0, 179,n.cyberneticscore,{n.cyberneticscore, n.fleetbeacon, n.airweapons2}, 1, false),
			AssetStats(n.airarmor3, 300, 300, 0,0, 179,n.cyberneticscore,{n.cyberneticscore, n.fleetbeacon, n.airarmor1}, 1, false),
			AssetStats(n.shields3, 300, 300, 0,0, 179, n.forge,{n.twilightcouncil, n.forge, n.shields2}, 1, false),
			AssetStats(n.charge, 100, 100, 0,0, 100, n.twilightcouncil,{n.twilightcouncil}, 1, false),
			AssetStats(n.graviticdrive, 100, 100, 0,0, 57,n.roboticsbay,{n.roboticsbay}, 1, false),
			AssetStats(n.resonatingglaives, 100, 100, 0,0, 100,n.twilightcouncil,{n.twilightcouncil}, 1, false),
			AssetStats(n.graviticboosters, 100, 100, 0,0, 57,n.roboticsbay,{n.roboticsbay}, 1, false),
			AssetStats(n.fluxvanes, 100, 100, 0,0, 57, n.fleetbeacon,{n.fleetbeacon}, 1, false),
			AssetStats(n.anionpulsecrystals, 150, 150, 0,0, 64,n.fleetbeacon,{n.fleetbeacon}, 1, false),
			AssetStats(n.extendedthermallance, 150, 150, 0,0, 100,n.roboticsbay,{n.roboticsbay}, 1, false),
			AssetStats(n.psionicstorm, 200, 200, 0,0, 79,n.templararchives,{n.templararchives}, 1, false),
			AssetStats(n.blink, 150, 150, 0, 0,121, n.twilightcouncil,{n.twilightcouncil}, 1, false),
			AssetStats(n.shadowstride, 100, 100, 0,0, 100,n.darkshrine,{n.darkshrine}, 1, false),
			AssetStats(n.warpgateresearch, 50, 50, 0, 0,100,n.cyberneticscore,{n.cyberneticscore}, 1, false),
			AssetStats(n.gravitoncatapult, 150, 150, 0,0, 57,n.fleetbeacon,{n.fleetbeacon}, 1, false),
		};
	}

	void initGoalState() {
		for (int i = 0; i < assetList.size(); i++) {
			goalState.push_back(0);
		}
		goalState[n.probe] = 14;
		goalState[n.zealot] = 1;
		goalState[n.sentry] = 3;
	}
	void initGlobalState() {
		minerals = 50;
		gas = 0;
		mProbeCount = 0;
		gProbeCount = 0;
		time = 0;

		//supply related items
		supply = 0;
		maxSupply = 0;
		for (Entity const& e : entityList) {
			if (e.assetType == n.probe) {
				mProbeCount++;
			}
			maxSupply += assetList[e.assetType].supProvide;
			supply += assetList[e.assetType].supCost;
		}
		maxFutureSupply = maxSupply;
	}
	void initEntityList() {
		entityList.push_back(loadEntity(n.dummy, 0, 0, true));
		entityList.push_back(loadEntity(n.nexus, 0, 0, true));
		entityList.back().energy = 50;
		state[n.nexus]++;
		for (int i = 0; i < 12; i++) {
			entityList.push_back(loadEntity(n.probe, 0, 0, true));
			state[n.probe]++;
		}
	}
	void copyEntityList(const vector<Entity>& origList) {
		for (const Entity& e : origList) {
			entityList.push_back(Entity(e));
		}
	}
	void reset() {
		entityList.clear();
		time = 0;
		for (int i = 0; i < state.size(); i++) {
			state[i] = 0;
		}
		initEntityList();
		initGlobalState();
	}
	Entity loadEntity(int action, int executor, int target, bool complete) {
		double timeToComplete;
		if (complete) {
			timeToComplete = 0;
		}
		else {
			double timeReduce = 0;
			if (executor > 0 && entityList[executor].timeChronoLeft > 0) {
				timeReduce = min(10, assetList[action].duration / 3);
			}
			timeToComplete = assetList[action].duration + time - timeReduce;
		}
		return Entity(action, timeToComplete, time, 0, 0, executor, target, complete);
	}
	void step(int action, int executor, int chronoTarget) {
		double timeToAction = computeTimeToAction(action, executor, chronoTarget);
		double slidingTime = timeToAction;
		//need to iterate through all incomplete items
		while (true) {
			int idx = getNextComplete();
			if (idx == -1) break;
			double timeComplete = entityList[idx].timeToComplete - time;
			if (timeComplete <= slidingTime) {
				elapseTime(timeComplete);
				completeEvent(idx);
				slidingTime = computeTimeToAction(action, executor, chronoTarget);
			}
			else break;
		}
		elapseTime(slidingTime);
		completeAction(action, executor, chronoTarget);
		//done = isDone();
	}

	void step(int action) {
		//assume default executor and chrono target
		vector<int> viableExecutors = getViableExecutors(action);
		if (action == n.chronoboost) {
			int executor = pickNextExecutor(viableExecutors);
			vector<int> viableTargets = getViableTargets(action, executor);
			int target = viableTargets[rand() % viableTargets.size()];
			step(action, executor, target);

		}
		else {
			int executor = pickNextExecutor(viableExecutors);
			step(action, executor, -1);
		}

	}

	double getTimeNextSupplyDone() {
		double minTime = 10000;
		for (const Entity& e : entityList) {
			if (!e.isComplete && assetList[e.assetType].supProvide > 0) {
				minTime = min(e.timeToComplete, minTime);
			}
		}
		return minTime - time;
	}

	double computeTimeToAction(int action, int executor, int chronoTarget) {
		if (action == n.chronoboost) {
			double energyAvailableAt;
			if (entityList[executor].isComplete) {
				energyAvailableAt = max(0.0, 50 - entityList[executor].energy) / REGEN_RATE;
			}
			else {
				energyAvailableAt = entityList[executor].timeToComplete - time;
			}
			return max(entityList[chronoTarget].timeChronoLeft, energyAvailableAt);
		}

		double timeMinerals;
		double timeGas;
		double timeSupply;
		double timeQueue;
		const AssetStats& a = assetList[action];
		double mineralRate = mRate();
		double gasRate = gRate();

		//also need to consider when executor has a free queue

		if (mineralRate == 0) timeMinerals = 0;
		else {
			timeMinerals = (a.minCost - minerals) / mineralRate;
		}
		if (gasRate == 0) timeGas = 0;
		else {
			timeGas = (a.gasCost - gas) / gasRate;
		}
		if (maxSupply >= supply + a.supCost) timeSupply = 0;
		else {
			timeSupply = getTimeNextSupplyDone();
		}
		if (executor > 0) {
			timeQueue = entityList[executor].timeQueueFree - time;
		}
		else {
			timeQueue = 0;

		}
		double largest = timeMinerals;
		if (timeGas > largest) largest = timeGas;
		if (timeSupply > largest) largest = timeSupply;
		if (timeQueue > largest) largest = timeQueue;
		return largest;
	}

	double mRate() {
		return mProbeCount;
	}
	double gRate() {
		return gProbeCount;
	}

	void elapseTime(double timeElapse) {
		minerals += timeElapse * mRate();
		gas += timeElapse * gRate();
		for (Entity& e : entityList) {
			//e.timeChronoLeft = max(0.0, e.timeChronoLeft - timeElapse);
			//e.timeQueueFree = max(0.0, e.timeQueueFree - timeElapse);
			//e.timeToComplete = max(0.0, e.timeToComplete - timeElapse);
			e.energy = min(200.0, e.energy + timeElapse * REGEN_RATE);
		}
		time += timeElapse;
	}

	void completeEvent(int idx) {
		int aType = entityList[idx].assetType;
		if (aType == n.nexus) {
			entityList[idx].energy = 50;
		}
		else if (aType == n.probe) {
			mProbeCount++;
		}
		else if (aType == n.assimilator) {
			int probesChange = max(0, min(3, mProbeCount - 3));
			mProbeCount -= probesChange;
			gProbeCount += probesChange;
		}
		maxSupply += assetList[entityList[idx].assetType].supProvide;
		entityList[idx].isComplete = true;
	}

	void completeAction(int action, int executor, int target) {
		if (action == n.chronoboost) {
			entityList[executor].energy -= 50;
			entityList[target].timeChronoLeft = 20;
			double timeStillQueued = max(0.0, entityList[target].timeQueueFree - time);
			double timeShift = min(10.0, timeStillQueued / 3);
			entityList[target].timeQueueFree -= timeShift;
			if (entityList[target].child > 0) {
				//production structure is currently building a unit
				entityList[entityList[target].child].timeToComplete -= timeShift;
			}
			return;
		}
		const AssetStats& a = assetList[action];
		maxFutureSupply += a.supProvide;
		minerals -= a.minCost;
		gas -= a.gasCost;
		supply += a.supCost;
		entityList.push_back(loadEntity(action, executor, target, false));
		if (executor > 0) {
			entityList[executor].timeQueueFree = a.duration + time;
			entityList[executor].child = entityList.size() - 1;
		}
		state[action] += 1;
	}

	int getNextComplete() {
		double minCompleteTime = 10000;
		int nextComplete = -1;
		for (int i = 0; i < entityList.size(); i++) {
			const Entity& e = entityList[i];
			if (!e.isComplete && e.timeToComplete < minCompleteTime) {
				minCompleteTime = e.timeToComplete;
				nextComplete = i;
			}
		}
		return nextComplete;
	}

	bool isDone() {
		//check if entity counter >= goalstate
		for (int i = 0; i < state.size(); i++) {
			if (state[i] < goalState[i]) {
				return false;
			}
		}
		return true;
	}

	double getTimeAllComplete() {
		double timeAllComplete = time;
		for (const Entity& e : entityList) {
			if (e.isComplete == false) {
				timeAllComplete = max(e.timeToComplete, timeAllComplete);
			}
		}
		return timeAllComplete;
	}

	bool techExists(int i) {
		for (int req : assetList[i].techReqs) {
			if (state[req] == 0) {
				return false;
			}
		}
		return true;
	}

	bool maxAssimilators(const AssetStats& a) {
		return (a.name == n.assimilator && state[n.assimilator] > state[n.nexus] * 2);
	}

	vector<int > getViableActions() {
		//needs to pass tech, supply, resource, maxCount checks
		//vector<int > viableActions;
		vector<int > viableActions(100);
		int viableCount = 0;
		for (const AssetStats& a : assetList) {
			if (maxAssimilators(a)) continue;
			bool techExists = true;
			for (int req : a.techReqs) {
				if (state[req] == 0) {
					techExists = false; break;
				}
			}
			bool isViable = (
				techExists
				&& (a.supCost + supply <= maxFutureSupply)
				&& (mProbeCount > 0 || a.minCost == 0)
				&& (gProbeCount > 0 || a.gasCost == 0)
				&& (state[a.name] < a.maxQuantity)
				);
			if (isViable) {
				viableActions[viableCount++] = a.name;
			}
		}
		//chronoboost
		if (state[n.nexus] > 0) {
			viableActions[viableCount++] = n.chronoboost;
		}
		viableActions.resize(viableCount);
		return viableActions;
	}

	vector<int> getEssentialActions() {
		//return all viable actions where goal state > current state
		vector<int> viableActions = getViableActions();
		vector<int > essentialActions(100);
		int essentialCount = 0;
		for (int i : viableActions) {
			if (i != n.chronoboost && goalState[i] > state[i]) {
				essentialActions[essentialCount++] = i;
			}
		}
		essentialActions.resize(essentialCount);
		return essentialActions;
	}

	vector<int> getViableExecutors(int action) {
		int executorName;
		if (action == n.chronoboost) {
			executorName = n.nexus;
		}
		else { executorName = assetList[action].parent; }
		vector<int> viableExecutors;
		if (executorName == n.dummy) return viableExecutors;
		for (int i = 0; i < entityList.size(); i++) {
			if (entityList[i].assetType == executorName) {
				viableExecutors.push_back(i);
			}
		}
		return viableExecutors;
	}

	vector<int> getViableTargets(int action, int executor) {
		vector<int> viableTargets;
		//only chronoboost has targets
		if (action != n.chronoboost) return viableTargets;
		for (int i = 0; i < entityList.size(); i++) {
			if (assetList[entityList[i].assetType].canChrono) {
				viableTargets.push_back(i);
			}
		}
		return viableTargets;
	}

	vector<vector<double>> getState() {
		int maxEntities = 100;
		vector<vector<double>> returnState(maxEntities, vector<double>(6, 0));
		for (int i = 0; i < entityList.size(); i++) {
			if (i == maxEntities)break;
			returnState[i][0] = entityList[i].assetType;
			returnState[i][1] = max(0.0, entityList[i].timeToComplete - time);
			returnState[i][2] = max(0.0, entityList[i].timeQueueFree - time);
			returnState[i][3] = max(0.0, entityList[i].timeChronoLeft - time);
			returnState[i][4] = entityList[i].energy;
			returnState[i][5] = (double)entityList[i].isComplete;
		}
		return returnState;
	}

	int pickNextExecutor(vector<int> viableExecutors) {
		if (viableExecutors.size() == 0) return -1;
		double timeFree = 10000;
		int nextExecutor = 0;
		for (int x : viableExecutors) {
			if (entityList[x].timeQueueFree < timeFree) {
				timeFree = entityList[x].timeQueueFree;
				nextExecutor = x;
			}
		}
		return nextExecutor;
	}
};

Names ProtossMacroEnv::n;
double ProtossMacroEnv::REGEN_RATE;
vector<AssetStats> ProtossMacroEnv::assetList;
int ProtossMacroEnv::ACTION_SPACE;

namespace py = pybind11;

PYBIND11_MODULE(probotest1, m) {
    m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------

        .. currentmodule:: probotest1

        .. autosummary::
           :toctree: _generate

    )pbdoc";

	/*pybind11::class_<Test>(m, "Test")
		.def(pybind11::init<>())
		;*/

    pybind11::class_<ProtossMacroEnv>(m, "ProtossMacroEnv")
		.def(pybind11::init<>())
		.def(pybind11::init<const ProtossMacroEnv&>(), "constuctor 2", pybind11::arg("env"))
        .def("step", &ProtossMacroEnv::step)
		.def("reset", &ProtossMacroEnv::reset)
		.def("getEntityList", &ProtossMacroEnv::getState)
		.def("getViableActions", &ProtossMacroEnv::getViableActions)
		.def("getViableExecutors", &ProtossMacroEnv::getViableExecutors)
		.def("pickNextExecutor", &ProtossMacroEnv::pickNextExecutor)
		.def("getTimeAllComplete", &ProtossMacroEnv::getTimeAllComplete)
		.def("getEssentialActions", &ProtossMacroEnv::getEssentialActions)
		.def("isDone",&ProtossMacroEnv::isDone)
        .def_readwrite("minerals", &ProtossMacroEnv::minerals)
		.def_readwrite("gas", &ProtossMacroEnv::gas)
		.def_readwrite("time", &ProtossMacroEnv::time)
		.def_readwrite("supply", &ProtossMacroEnv::supply)
		.def_readwrite("supplycap", &ProtossMacroEnv::maxSupply)
		.def_readwrite("probeCountOnMinerals", &ProtossMacroEnv::mProbeCount)
		.def_readwrite("probeCountOnGas", &ProtossMacroEnv::gProbeCount)
		.def_readwrite("state", &ProtossMacroEnv::state)
		.def_readwrite("goalState", &ProtossMacroEnv::goalState)
        ;

	pybind11::class_<Names>(m, "Names")
		.def(pybind11::init<>())
		.def_readwrite("dummy", &Names::dummy)
		.def_readwrite("probe", &Names::probe)
		.def_readwrite("zealot", &Names::zealot)
		.def_readwrite("sentry", &Names::sentry)
		.def_readwrite("stalker", &Names::stalker)
		.def_readwrite("adept", &Names::adept)
		.def_readwrite("hightemplar", &Names::hightemplar)
		.def_readwrite("darktemplar", &Names::darktemplar)
		.def_readwrite("observer", &Names::observer)
		.def_readwrite("warpprism", &Names::warpprism)
		.def_readwrite("immortal", &Names::immortal)
		.def_readwrite("colossus", &Names::colossus)
		.def_readwrite("disruptor", &Names::disruptor)
		.def_readwrite("phoenix", &Names::phoenix)
		.def_readwrite("voidray", &Names::voidray)
		.def_readwrite("oracle", &Names::oracle)
		.def_readwrite("tempest", &Names::tempest)
		.def_readwrite("carrier", &Names::carrier)
		.def_readwrite("warpzealot", &Names::warpzealot)
		.def_readwrite("warpsentry", &Names::warpsentry)
		.def_readwrite("warpstalker", &Names::warpstalker)
		.def_readwrite("warpadept", &Names::warpadept)
		.def_readwrite("warphightemplar", &Names::warphightemplar)
		.def_readwrite("warpdarktemplar", &Names::warpdarktemplar)
		.def_readwrite("nexus", &Names::nexus)
		.def_readwrite("pylon", &Names::pylon)
		.def_readwrite("assimilator", &Names::assimilator)
		.def_readwrite("gateway", &Names::gateway)
		.def_readwrite("forge", &Names::forge)
		.def_readwrite("photoncannon", &Names::photoncannon)
		.def_readwrite("shieldbattery", &Names::shieldbattery)
		.def_readwrite("warpgate", &Names::warpgate)
		.def_readwrite("cyberneticscore", &Names::cyberneticscore)
		.def_readwrite("twilightcouncil", &Names::twilightcouncil)
		.def_readwrite("roboticsfacility", &Names::roboticsfacility)
		.def_readwrite("stargate", &Names::stargate)
		.def_readwrite("templararchives", &Names::templararchives)
		.def_readwrite("darkshrine", &Names::darkshrine)
		.def_readwrite("roboticsbay", &Names::roboticsbay)
		.def_readwrite("fleetbeacon", &Names::fleetbeacon)
		.def_readwrite("groundweapons1", &Names::groundweapons1)
		.def_readwrite("groundarmor1", &Names::groundarmor1)
		.def_readwrite("airweapons1", &Names::airweapons1)
		.def_readwrite("airarmor1", &Names::airarmor1)
		.def_readwrite("shields1", &Names::shields1)
		.def_readwrite("groundweapons2", &Names::groundweapons2)
		.def_readwrite("groundarmor2", &Names::groundarmor2)
		.def_readwrite("airweapons2", &Names::airweapons2)
		.def_readwrite("airarmor2", &Names::airarmor2)
		.def_readwrite("shields2", &Names::shields2)
		.def_readwrite("groundweapons3", &Names::groundweapons3)
		.def_readwrite("groundarmor3", &Names::groundarmor3)
		.def_readwrite("airweapons3", &Names::airweapons3)
		.def_readwrite("airarmor3", &Names::airarmor3)
		.def_readwrite("shields3", &Names::shields3)
		.def_readwrite("charge", &Names::charge)
		.def_readwrite("graviticdrive", &Names::graviticdrive)
		.def_readwrite("resonatingglaives", &Names::resonatingglaives)
		.def_readwrite("graviticboosters", &Names::graviticboosters)
		.def_readwrite("fluxvanes", &Names::fluxvanes)
		.def_readwrite("anionpulsecrystals", &Names::anionpulsecrystals)
		.def_readwrite("extendedthermallance", &Names::extendedthermallance)
		.def_readwrite("psionicstorm", &Names::psionicstorm)
		.def_readwrite("blink", &Names::blink)
		.def_readwrite("shadowstride", &Names::shadowstride)
		.def_readwrite("warpgateresearch", &Names::warpgateresearch)
		.def_readwrite("gravitoncatapult", &Names::gravitoncatapult)
		.def_readwrite("chronoboost", &Names::chronoboost)
		;


#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
