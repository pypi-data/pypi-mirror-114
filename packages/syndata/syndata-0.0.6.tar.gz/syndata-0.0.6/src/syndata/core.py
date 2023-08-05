import numpy as np
import scipy.stats as stats

class ClusterData:
	"""
	Generates data sets with clusters according to user specifications.

	Parameters
	----------
	n_clusters : int
		Number of clusters
	n_dim : int
		Dimensionality of data points
	n_sample : int
		Total number of data points 
	class_bal : ClassBal object
		Defines relative class sizes (samples sizes for each cluster)
	cov_geom : CovGeom object
		Defines cluster covariance structures
	center_geom : CenterGeom object
		Defines placement of cluster centers
	data_dist : DataDist object
		Defines probability distribution for data
	scale : float, optional
		Sets reference length scale for simulated data

	Attributes
	----------
	class_sizes :
	cluster_axes :
	cluster_sd :
	cov : 
	cov_inv :
	data :

	"""
		
	def __init__(self, n_clusters, n_dim, n_samples, class_bal, cov_geom, 
		center_geom, data_dist, scale=1.0):
		"""
		Constructs a ClusterData object.
		"""
		self.n_clusters = n_clusters
		self.n_dim = n_dim
		self.n_samples = n_samples
		self.class_bal = class_bal
		self.cov_geom = cov_geom
		self.center_geom = center_geom
		self.data_dist = data_dist
		self.data = None
		self.labels = None
		self.centers = None
		self.class_sizes = None
		self.cov = None
		self.cov_inv = None
		self.cluster_axes = None
		self.cluster_sd = None
		self.scale = scale

	def to_csv(self, filename):
		"""
		Writes data to a csv file.
		"""
		if (self.data is None):
			print('Error: No data has been generated. Call ClusterData.generate_data to generate data.')
		else:
			np.savetxt(filename, self.data, delimiter=',')
		
		
	def generate_data(self,sparse=False, noise_factor=1.0, mode='sparse'):
		"""
		Generates a data set with clusters according to a ClusterData object.
		
		Parameters
		----------
		self : ClusterData
			Defines how data is generated
		sparse : bool
			Decide whether to add noise covariates to the data
		noise_factor : float
			Determines the number of noise covariates added, if sparse=True 
		mode : str
			Determines the meaning of noise_factor


		Returns
		-------
		X : (self.n_samples, 1+self.n_dim) ndarray
			Data matrix whose rows are the data points. The last column stores the 
			cluster labels as integers from 0 to self.n_clusters.
		"""
		print('Compute class sizes...')
		self.class_sizes = self.class_bal.make_class_sizes(self)

		print('Compute covariance structures...')
		axes, sd, cov, cov_inv = self.cov_geom.make_cov(self)
		self.cluster_axes = axes
		self.cluster_sd = sd
		self.cov = cov
		self.cov_inv = cov_inv

		print('Place cluster centers...')
		self.centers = self.center_geom.place_centers(self)

		print('Sample data...')
		self.data, self.labels = self.data_dist.sample(self)

		print('Success!')

		if sparse:
			self.data = self.add_noise(self.data,noise_factor=noise_factor,mode=mode)

		return (self.data, self.labels)


	def add_noise(self, noise_factor, mode='sparse', model='gaussian'):
		"""
		Add noise covariates to data set.

		If mode='sparse', noise_factor is the ratio between the number
		of noise covariates vs meaningful covariates. If mode='dim',
		noise_factor is the ratio between the total number of covariates
		and the number of samples, i.e. a high noise_factor indicates
		high-dimensional data in the statistical sense (more covariates 
		than samples).
		"""

		X = self.data
		mean_of_std = np.mean(np.array(self.cluster_sd))
		std_of_std = np.std(np.array(self.cluster_sd))

		n_dim = X.shape[1] 
		n_samples = X.shape[0]
		#all_obs = X.reshape((X.size,))
		#std_obs = np.std(all_obs); mean_obs = np.mean(all_obs)

		if (mode == 'sparse'):
			n_noise_cov = int(np.ceil(n_dim * noise_factor))
			synthetic_std = np.abs(np.random.normal(loc=mean_of_std, scale=std_of_std, size=n_noise_cov))
			noise_cov = np.random.normal(loc=0, scale=synthetic_std, size=(n_samples,n_noise_cov))
			return np.concatenate([X,noise_cov],axis=1)
		elif (mode == 'dim'):
			n_cov = int(np.ceil(n_samples * noise_factor))
			n_noise_cov = n_cov - n_dim
			if (n_noise_cov <= 0):
				print("Given data is already more high-dimensional than desired! No changes were made.")
				return X
			else:
				synthetic_std = np.abs(np.random.normal(loc=mean_of_std, scale=std_of_std, size=n_noise_cov))
				noise_cov = np.random.normal(loc=0, scale=synthetic_std, size=(n_samples,n_noise_cov))
				return np.concatenate([X,noise_cov],axis=1)



class CovGeom:
	"""
	Specifies the covariance structure for ClusterData.
	"""
	
	def __init__(self, clusterdata):
		pass

	def make_cov(self):
		pass

	def make_orthonormal_axes(self, n_dim, n_axes):
		"""
		Samples orthonormal axes for cluster generation.
		Creates n_axes orthonormal axes in n_dim-dimensional space.

		Parameters
		----------
		n_dim : int
			Dimensionality of the data space
		n_axes : int
			Number of axes to generate

		Returns
		-------
		out : (n_axes, n_dim) ndarray
			Each row is an axis.
		"""
		ortho_matrix = stats.ortho_group.rvs(n_dim)
		return ortho_matrix[:n_axes, :]



class CenterGeom:
	"""
	Defines placement of cluster centers for ClusterData.
	"""

	def __init__(self, clusterdata):
		pass

	def make_centers(self):
		pass



class ClassBal:
	"""
	Specifies the relative cluster sizes for ClusterData.
	"""

	def __init__(self):
		pass

	def make_class_sizes(self, clusterdata):
		pass



class DataDist:
	"""
	Defines data probability distribution for ClusterData.
	"""

	def __init__(self):
		pass

	def sample(self, clusterdata):
		n_clusters = clusterdata.n_clusters
		n_samples = clusterdata.n_samples
		n_dim = clusterdata.n_dim
		class_sizes = clusterdata.class_sizes
		centers = clusterdata.centers

		axes = clusterdata.cluster_axes
		sd = clusterdata.cluster_sd

		X = np.full(shape=(n_samples, n_dim), fill_value=np.nan)
		y = np.full(n_samples, fill_value=np.nan).astype(int)

		start = 0
		for i in range(n_clusters):
			end = start + class_sizes[i]
			# Set class label
			y[start:end] = i
			# Sample data
			X[start:end,:] = self.sample_cluster(cluster_size=class_sizes[i], 
										  mean=centers[i], axes=axes[i],
										  sd=sd[i])
			start = end

		return (X, y)

	def sample_cluster(self,cluster_size, mean,axes,sd):
		pass