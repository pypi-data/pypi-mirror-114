'''
Uses the eigenvalues file generated by Octopus and makes its information
available to use

Information contained in bandstructure file
-------------------------------------------
eigenvalues -> occupation, number of occupied bands
'''

import re
import numpy as np

class Eigenvalues():
    '''
    Class that holds and gives methods to the information of an eigenvalues
    file

    Attributes:
      _eigenvalues (list string): holds all the data of the eigenvalues file in a list
      _eigenvalues_path (string): filepath with the addition of the eigenvalues file
      _num_bands (int): number of bands
      _num_kpoints (int): number of kpoints
      num_occ_bands (int): number of occupied bands
      occupancies (numpy array): of shape (num_kpoints, num_bands) type (float64)
    '''

    def __init__(self, filepath, num_kpoints, num_bands):
        '''
        Args:
          filepath (string): filepath to find eigenvalues file
          num_kpoints (int): number of kpoints
          num_bands (int): number of bands
        '''
        
        self._eigenvalues = None
        self._eigenvalues_path = filepath + 'eigenvalues'
        self._num_bands = num_bands
        self._num_kpoints = num_kpoints
        self._partials_mask = None
        self.num_occ_bands = None
        self.occupancies = None
        self._load_eigenvalues()


    def get_occupancies(self):
        '''
        Extracts the occupancies from the eigenvalue data. If partial occupancies are
        found they are set to zero and occupied bands are set to 2.0

        Returns:
          occupancies (numpy array): of shape (num_kpoints, num_bands) type (float64)
        '''

        # find the index of the match and get numkpoints of lines results
        pattern = '#st  Spin   Eigenvalue+\s+[a-zA-Z]+.+Error$'
        matched_idx = [idx for idx, item in enumerate(self._eigenvalues) if re.search(pattern, item)]
        start = matched_idx[0]

        # start at the second line not including the matched text
        eigenvalues_table = self._eigenvalues[start:][1:]

        # remove the kpoint lines
        eigenvalues_table = [value for value in eigenvalues_table if '#k' not in value]

        # place the occupancies into a numpy array
        occupancy_list = [row.split()[3] for row in eigenvalues_table]
        occupancies = np.array(occupancy_list)

        # change to shape (num_kpoints, num_bands) and data type to float64
        occupancies.shape = (self._num_kpoints, self._num_bands)
        self.occupancies = occupancies.astype('float64')

        # check for partial occupancies
        # create a masked array with True for not partial and False for partial occupancies
        self._partials_mask = np.ones((self._num_bands, ),dtype=bool) 
        for kpoint_occupancies in self.occupancies:
            partial, mask = self._check_partial_occupancies(kpoint_occupancies)

            # creates a long array of shape (num_kpoints*num_bands, )
            # shape doesnt matter we just want to check for False values
            self._partials_mask = np.append(self._partials_mask, mask, axis = 0)

        # if there are partial occupancies found floor all the occupancies to
        # remove any partial occupancies and set occupied bands to 2.0
        if not (self._partials_mask == True).all():
            print('partial occupancies found...')
            self.occupancies = np.floor(self.occupancies)
            num_occ_bands = self.get_num_occ_bands()
            self.occupancies[:, :num_occ_bands] = 2.0

        return(self.occupancies)

    def get_num_occ_bands(self):
        '''
        Extracts the number of occupied bands from the occupancy array
        
        Returns:
          num_occ_bands (int): Number of occupied bands
        '''
        
        for kpoint_occupancies in self.occupancies:
            
            # make sure the number of occupied bands isnt calculated from
            # partial occupancies
            if self._check_partial_occupancies(kpoint_occupancies)[0]:
                num_occ_bands = np.count_nonzero(kpoint_occupancies)
                break

        self.num_occ_bands = num_occ_bands

        return(self.num_occ_bands)

    def _check_partial_occupancies(self, kpoint_occupancies):
        '''
        Checks each array for a partial occupancy and returns boolean
        and masked array no partial occupancy (True), partial occupancy (False)

        Params:
            kpoint_occupancies (numpy array): shape (num_bands, )

        Returns:
            boolean
            mask (numpy, array): shape (num_bands, )
        '''

        # Create a mask of elements with a nonzero decimal component
        masking = np.zeros(shape=kpoint_occupancies.shape)
        np.mod(kpoint_occupancies, 1, out=masking)
        mask = (masking == 0)

        return((mask==True).all(), mask)

    def _load_eigenvalues(self):
        '''
        Loads the eigenvalues file as a list of lines

        Returns:
          eigenvalues (list string): list of lines from eigenvalues
        '''

        f = open(self._eigenvalues_path, 'r')
        text = f.read()

        # creates a list of lines rather than a long string with newline characters
        self._eigenvalues = text.splitlines()
        f.close()